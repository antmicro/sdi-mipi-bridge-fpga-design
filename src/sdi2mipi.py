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


from migen import *
from migen.fhdl import verilog
from migen.fhdl.module import Module
from migen.genlib.cdc import MultiReg

from divider import Divider
from aligner import Aligner
from detector import DetectTRS
from timing_gen import create_timing_generator
from common import UnsupportedVideoFormatException

__all__ = ["SDI2MIPI"]


class SDI2MIPI(Module):
    supported_video_formats = ["720p60", "1080p25", "1080p30", "1080p50", "1080p60"]

    def __init__(self, video_format="720p60", four_lanes=False, sim=False):
        if video_format not in self.supported_video_formats:
            raise UnsupportedVideoFormatException(self.supported_video_formats)

        self.clk = ClockSignal()
        self.rst = ResetSignal()
        self.vsync_i = Signal(name="vsync_i")
        self.hsync_i = Signal(name="hsync_i")
        self.data_i = Signal(8, name="data_i")
        self.fv_o = Signal(name="fv_o")
        self.lv_o = Signal(name="lv_o")

        self.ios = {
            self.vsync_i,
            self.hsync_i,
            self.data_i,
            self.fv_o,
            self.lv_o,
        }

        # logic
        pix_clk = Signal()
        pix_rst = Signal()

        if video_format in ["720p60", "1080p25", "1080p30"]:
            align_sig = Signal()
            if not sim:
                # fmt: off
                self.specials += Instance(
                    "CLKDIVG",
                    p_DIV     = "2.0",
                    p_GSR     = "DISABLED",
                    i_RST     = self.rst,
                    i_CLKI    = self.clk,
                    i_ALIGNWD = align_sig,
                    o_CDIVX   = pix_clk
                )
                # fmt: on
            else:
                self.submodules.divider = Divider()
                self.comb += [
                    self.divider.mode_i.eq(align_sig),
                    pix_clk.eq(self.divider.pix_clk_o),
                ]
        else:
            self.comb += pix_clk.eq(self.clk)
        self.comb += pix_rst.eq(self.rst)

        timing_generator = create_timing_generator(video_format, four_lanes)
        self.submodules.timing_gen = timing_generator
        self.comb += [
            self.timing_gen.pix.clk.eq(pix_clk),
            self.timing_gen.pix.rst.eq(pix_rst),
            self.timing_gen.vsync_i.eq(self.vsync_i),
            self.timing_gen.hsync_i.eq(self.hsync_i),
            self.fv_o.eq(self.timing_gen.fv_o),
            self.lv_o.eq(self.timing_gen.lv_o),
        ]

        if video_format == "720p60":
            n_align = Signal()
            detector_rst = Signal()

            self.submodules.detector = DetectTRS()
            self.comb += [
                self.detector.pix.clk.eq(pix_clk),
                self.detector.pix.rst.eq(pix_rst),
                self.detector.det.clk.eq(self.clk),
                self.detector.det.rst.eq(detector_rst),
                self.detector.lv_i.eq(self.lv_o),
                n_align.eq(self.detector.n_align_o),
            ]

            self.submodules.aligner = Aligner()
            self.comb += [
                self.aligner.n_align_i.eq(n_align),
                align_sig.eq(self.aligner.align_o),
                detector_rst.eq(self.aligner.detector_rst_o),
            ]


if __name__ == "__main__":
    sdi_mipi = SDI2MIPI()
    print(verilog.convert(sdi_mipi, sdi_mipi.ios, name="sdi2mipi"))
