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

from migen.fhdl.verilog import convert
from migen.fhdl.decorators import ResetInserter, ClockDomainsRenamer

from migen import *


class DetectTRS(Module):
    """
    A state machine module for detecting EAV packets located in
    vertical blanking. EAV detection is used for checking data alignment.
    """

    def __init__(self):
        # IOs
        self.data_i = Signal(8)
        self.lv_i = Signal()
        self.n_align_o = Signal()
        self.detector_rst = Signal()

        # Sys clock divided by 2
        # effectively a pixel clock compliant with VESA timings
        self.clock_domains.det = ClockDomain(name="det")
        self.clock_domains.pix = ClockDomain(name="pix")

        self.ios = {
            self.det.clk,
            self.det.rst,
            self.pix.clk,
            self.pix.rst,
            self.data_i,
            self.lv_i,
            self.n_align_o,
        }

        # Input/Output list for correct module generation
        # Flags for checking word alignment
        F1 = Signal()
        F2 = Signal()
        F3 = Signal()

        detect_trs = Signal()
        s1 = Signal()
        s2 = Signal(2)
        s3 = Signal()

        # Detect EAV preamble: 0xFF 0xFF 0x0 0x0 0x0 0x0 0xB6 0xB6
        detect = ClockDomainsRenamer("det")(FSM(reset_state="FIRST_OK"))
        self.submodules += detect
        detect_trs.eq(detect.ongoing("DONE"))

        # fmt: off
        detect.act("FIRST_OK",
            detect_trs.eq(0),
            If(~self.lv_i,
                If(self.data_i == 0xFF,
                    If(s1 < 1,
                        NextValue(s1, s1 + 1),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("FIRST_OK"),
                    ).Else(
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("SECOND_OK"),
                        If(self.pix.clk,
                            NextValue(F1, 1),
                        ).Else(
                            NextValue(F1, 0),
                        ),
                    ),
                ).Else(
                    NextValue(s1, 0),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ),
            ).Else(
                NextValue(s1, 0),
                NextValue(s2, 0),
                NextValue(s3, 0),
                NextState("FIRST_OK"),
            ),
        )

        detect.act("SECOND_OK",
            detect_trs.eq(0),
            If(~self.lv_i,
                If(self.data_i == 0x0,
                    If(s2 < 3,
                        NextValue(s1, 0),
                        NextValue(s2, s2 + 1),
                        NextValue(s3, 0),
                        NextState("SECOND_OK"),
                    ).Else(
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("THIRD_OK"),
                        If(self.pix.clk,
                            NextValue(F2, 1),
                        ).Else(
                            NextValue(F2, 0),
                        ),
                    ),
                ).Elif(self.data_i == 0xFF,
                    NextValue(s1, 1),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ).Else(
                    NextValue(s1, 0),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ),
            ).Else(
                NextValue(s1, 0),
                NextValue(s2, 0),
                NextValue(s3, 0),
                NextState("FIRST_OK"),
            ),
        )

        detect.act("THIRD_OK",
            detect_trs.eq(0),
            If(~self.lv_i,
                # Detect XY byte for EAV in vertical blanking: 0xB6
                If((self.data_i & 0xF0) == 0xB0,
                    If(s3 < 1,
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, s3 + 1),
                        NextState("THIRD_OK"),
                    ).Else(
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("DONE"),
                        If(self.pix.clk,
                            NextValue(F3, 1),
                        ).Else(
                            NextValue(F3, 0),
                        ),
                    ),
                ).Elif(
                    self.data_i == 0xFF,
                    NextValue(s1, 1),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ).Else(
                    NextValue(s1, 0),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ),
            ).Else(
                NextValue(s1, 0),
                NextValue(s2, 0),
                NextValue(s3, 0),
                NextState("FIRST_OK"),
            ),
        )

        detect.act("DONE",
            detect_trs.eq(1),
        )
        # fmt: on

        # Check alignment
        self.sync.det += [If(detect_trs & F1 & F2 & F3, self.n_align_o.eq(1))]


if __name__ == "__main__":
    detect = DetectTRS()
    print(convert(detect, detect.ios, name="detector"))
