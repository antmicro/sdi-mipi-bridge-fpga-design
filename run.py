#!/usr/bin/env python3
# Copyright 2023 Antmicro <www.antmicro.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys

sys.path.append("src")

import shutil
import subprocess
import argparse

from top import Top
from migen.fhdl.verilog import convert


def run_diamondc(tcl_script_path, **kwargs):
    if not os.path.isfile(tcl_script_path):
        raise FileNotFoundError(f"Tcl script does not exist! ({tcl_script_path})")

    subprocess.check_call(f"diamondc {tcl_script_path}", shell=True, **kwargs)


def run_patch(patch, file, **kwargs):
    if not os.path.isfile(patch):
        raise FileNotFoundError(f"Patch file does not exist! ({patch})")

    if not os.path.isfile(file):
        raise FileNotFoundError(f"File does not exist! ({file})")

    subprocess.check_call(f"patch {file} {patch}", shell=True, **kwargs)


def prepare_cmos2dphy_sources(
    lattice_tpl_dir, patch_dir, output_dir, video_format="720p60", four_lanes=False
):

    # prepare paths

    lattice_dst_dir = os.path.abspath(os.path.join(output_dir, "lattice"))

    lanes_name_part = "4lanes" if four_lanes else "2lanes"
    config_dir_name = f"{video_format}-{lanes_name_part}"

    c2dphy_src_dir = os.path.join(lattice_tpl_dir, "CMOS2DPHY", config_dir_name)
    c2dphy_dst_dir = os.path.join(lattice_dst_dir, "CMOS2DPHY")

    files_to_copy = [
        {
            "src": os.path.join(c2dphy_src_dir, "CMOS2DPHY.sbx"),
            "dst": os.path.join(c2dphy_dst_dir, "CMOS2DPHY.sbx"),
        },
        {
            "src": os.path.join(lattice_tpl_dir, "CMOS2DPHY", "generate_core.tcl"),
            "dst": os.path.join(c2dphy_dst_dir, "csi2_inst", "generate_core.tcl"),
        },
        {
            "src": os.path.join(lattice_tpl_dir, "CMOS2DPHY", "CMOS2DPHY.v"),
            "dst": os.path.join(c2dphy_dst_dir, "CMOS2DPHY.v"),
        },
        {
            "src": os.path.join(c2dphy_src_dir, "csi2_inst.lpc"),
            "dst": os.path.join(c2dphy_dst_dir, "csi2_inst", "csi2_inst.lpc"),
        },
    ]

    # create project

    os.makedirs(output_dir, exist_ok=True)
    if os.path.isdir(lattice_dst_dir):
        shutil.rmtree(lattice_dst_dir)

    for entry in files_to_copy:
        os.makedirs(os.path.dirname(entry["dst"]), exist_ok=True)
        shutil.copyfile(entry["src"], entry["dst"])

    tcl_script_path = os.path.join(output_dir, "cmos2dphy_gen.tcl")
    tcl_script = [f"cd {lattice_dst_dir}/CMOS2DPHY/csi2_inst"]
    tcl_script += [f"source {lattice_dst_dir}/CMOS2DPHY/csi2_inst/generate_core.tcl"]

    with open(tcl_script_path, "w") as fd:
        fd.write("\n".join(tcl_script))
        fd.flush()
        run_diamondc(tcl_script_path, cwd=output_dir)

    if video_format == "1080p60":
        patch_path = os.path.abspath(
            os.path.join(patch_dir, config_dir_name, "csi2_inst.v.patch")
        )
        file_path = os.path.join(c2dphy_dst_dir, "csi2_inst", "csi2_inst.v")

        run_patch(patch_path, file_path, cwd=output_dir)


def prepare_diamond_project(
    output_dir,
    name,
    device,
    lpf_file,
    sources,
    sbx_path=None,
    sbx_inst_exp=[],
    synthesis_tool="lse",
):
    os.makedirs(output_dir, exist_ok=True)

    tcl_script_path = os.path.join(output_dir, "project.tcl")

    tcl_script = [
        f"prj_project new -name {name} -dev {device} -lpf {lpf_path} -synthesis {synthesis_tool}"
    ]
    tcl_script += ["prj_impl option top top"]

    for src in sources:
        tcl_script += [f"prj_src add {os.path.abspath(src)}"]

    if sbx_path is not None:
        tcl_script += [f"prj_src add {os.path.abspath(sbx_path)}"]

    tcl_script += ["prj_run Synthesis"]
    tcl_script += ["prj_run Export -task Bitgen"]

    tcl_script += ["prj_project save"]
    tcl_script += ["prj_project close"]

    with open(tcl_script_path, "w") as fd:
        fd.write("\n".join(tcl_script))
        fd.flush()
        run_diamondc(tcl_script_path, cwd=output_dir)


def prepare_top_sources(output_dir):
    top = Top()
    top_path = os.path.join(output_dir, "top.v")

    forward_bb_declarations = """
/* Forward black-box declarations for Diamond */
module OSCI (HFOUTEN, HFCLKOUT,LFCLKOUT);
parameter HFCLKDIV = 1;
input HFOUTEN;
input HFCLKOUT;
output LFCLKOUT;
endmodule

"""

    with open(top_path, "w") as fd:
        fd.write(forward_bb_declarations)
        fd.write(str(convert(top, top.ios, name="top")))


if __name__ == "__main__":

    # parse arguments

    parser = argparse.ArgumentParser(
        description="Generate gateware for SDI-MIPI Bridge Tester"
    )
    parser.add_argument(
        "--video-format",
        default="720p60",
        help='Video format ("720p60", "1080p30", or "1080p60")',
    )
    parser.add_argument(
        "--lanes", type=int, default=2, help='Number of lanes ("2", or "4")'
    )
    args = parser.parse_args()

    if args.video_format not in ("720p60", "1080p30", "1080p60"):
        sys.exit("Unsupported video format")

    if args.lanes not in (2, 4):
        sys.exit("Unsupported number of lanes")

    # constants for project

    PRJ_NAME = "sdi2mipi_tester"
    DEVICE = "LIF-MD6000-6KMG80I"
    CLARITY_DESIGN_NAME = "CMOS2DPHY"
    CMOS2DPHY_INST_NAME = "csi2_inst"

    # create names

    lanes_name_part = "4lanes" if args.lanes == 4 else "2lanes"
    output_dir_rel = os.path.join("build", f"{args.video_format}-{lanes_name_part}")

    output_dir = os.path.abspath(output_dir_rel)
    top_path = os.path.join(output_dir, "top.v")
    lattice_tpl_dir = os.path.abspath("lattice")
    patch_dir = os.path.abspath("patches")
    lpf_path = os.path.abspath(os.path.join("src", f"{PRJ_NAME}.lpf"))
    sbx_path = os.path.join(
        output_dir, "lattice", CLARITY_DESIGN_NAME, f"{CLARITY_DESIGN_NAME}.sbx"
    )

    # generate project

    srcs = [top_path]
    sbx_export_inst = [f"{CLARITY_DESIGN_NAME}/{CMOS2DPHY_INST_NAME}"]

    os.makedirs(output_dir, exist_ok=True)
    prepare_top_sources(output_dir)

    four_lanes = True if args.lanes == 4 else False
    prepare_cmos2dphy_sources(
        lattice_tpl_dir, patch_dir, output_dir, args.video_format, four_lanes
    )
    prepare_diamond_project(
        output_dir, PRJ_NAME, DEVICE, lpf_path, srcs, sbx_path, sbx_export_inst
    )
