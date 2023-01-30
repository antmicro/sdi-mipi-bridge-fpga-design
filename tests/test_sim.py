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

tests_dir = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.realpath(os.path.join(tests_dir, "..", "src"))
sys.path.append(src_path)

import logging
import pytest
import subprocess

from migen import *
from migen.fhdl.verilog import convert as convert_migen

from sdi2mipi import SDI2MIPI
from divider import Divider
from detector import DetectTRS
from aligner import Aligner
from timing_gen import create_timing_generator

log = logging.getLogger(__name__)

SIM_PARAMS = {
    "720p60": {
        "H_ACTIVE": "1280",
        "H_SYNC": "40",
        "H_BACK_PORCH": "220",
        "H_FRONT_PORCH": "110",
        "V_ACTIVE": "720",
        "V_SYNC": "5",
        "V_BACK_PORCH": "20",
        "V_FRONT_PORCH": "5",
        "FRAMES": "3",
        "PER": "13468",
        "MUL": "1",
    },
    "1080p30": {
        "H_ACTIVE": "1920",
        "H_SYNC": "44",
        "H_BACK_PORCH": "148",
        "H_FRONT_PORCH": "88",
        "V_ACTIVE": "1080",
        "V_SYNC": "5",
        "V_BACK_PORCH": "36",
        "V_FRONT_PORCH": "4",
        "FRAMES": "4",
        "PER": "13468",
        "MUL": "1",
    },
    "1080p60": {
        "H_ACTIVE": "1920",
        "H_SYNC": "44",
        "H_BACK_PORCH": "148",
        "H_FRONT_PORCH": "88",
        "V_ACTIVE": "1080",
        "V_SYNC": "5",
        "V_BACK_PORCH": "36",
        "V_FRONT_PORCH": "4",
        "FRAMES": "3",
        "PER": "6734",
        "MUL": "1",
    },
}


def params_to_iverilog_opts(params):
    opt_str = ""
    for k, v in params.items():
        opt_str += f"-P{k}={v} "
    return opt_str


def compile_simulation(output_path, srcs, options="", **kwargs):
    for src in srcs:
        if not os.path.isfile(src):
            raise FileNotFoundError(f"Source file does not exist! ({src})")

    output_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_dir):
        raise FileNotFoundError(f"Output directory does not exist! ({output_dir})")

    srcs_str = " ".join(srcs)
    cmd = f"iverilog -o {output_path} {options} {srcs_str}"
    print(cmd)
    subprocess.check_call(cmd, shell=True, **kwargs)


def run_simulation(sim_binary_path, options="", **kwargs):
    if not os.path.isfile(sim_binary_path):
        raise FileNotFoundError(
            f"Simulation binary does not exist! ({sim_binary_path})"
        )

    cmd = f"vvp {options} {sim_binary_path}"
    print(cmd)
    subprocess.check_call(f"vvp {options} {sim_binary_path}", shell=True, **kwargs)


def simulate_module(module, top_name, testbench_path, output_dir, iverilog_cmp_opts=""):
    output_dir = os.path.abspath(output_dir)
    verilog_output_path = os.path.join(output_dir, f"{top_name}.v")
    binary_output_path = os.path.join(output_dir, f"{top_name}.bin")

    os.makedirs(output_dir, exist_ok=True)
    srcs = [os.path.abspath(x) for x in (verilog_output_path, testbench_path)]

    convert_migen(module, module.ios, top_name).write(verilog_output_path)
    compile_simulation(
        binary_output_path, srcs, cwd=output_dir, options=iverilog_cmp_opts
    )
    run_simulation(binary_output_path, cwd=output_dir)


@pytest.mark.parametrize("four_lanes", [True, False])
@pytest.mark.parametrize("video_format", ["720p60", "1080p30", "1080p60"])
def test_sdi2mipi(four_lanes, video_format):
    sdi2mipi = SDI2MIPI(video_format=video_format, four_lanes=four_lanes, sim=True)
    iverilog_opts = params_to_iverilog_opts(SIM_PARAMS[video_format])
    simulate_module(
        sdi2mipi,
        "sdi2mipi",
        "sdi2mipi_tb.v",
        f"build/sdi2mipi/{video_format}",
        iverilog_opts,
    )


def test_aligner():
    aligner = Aligner()
    simulate_module(aligner, "aligner", "aligner_tb.v", f"build/aligner")


def test_detector():
    detector = DetectTRS()
    simulate_module(detector, "detector", "detector_tb.v", f"build/detector")


@pytest.mark.parametrize("video_format", ["720p60", "1080p30", "1080p60"])
def test_timing_gen(video_format):
    timing_gen = create_timing_generator(video_format)
    iverilog_opts = params_to_iverilog_opts(SIM_PARAMS[video_format])
    simulate_module(
        timing_gen, "timing_gen", "timing_gen_tb.v", f"build/timing_gen", iverilog_opts
    )
