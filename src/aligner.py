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
from migen import *


class Aligner(Module):
    """
    A module connected to detector and divider.
    It is forcing the delay as long as the data is not aligned
    """

    def __init__(self):
        self.detector_rst_o = Signal()
        self.n_align_i = Signal()
        self.align_o = Signal()

        # Input clock from deserializer
        # doubled pixel clock frequency for given resolution

        # Input/Output list for correct module generation
        self.ios = {self.n_align_i, self.align_o, self.detector_rst_o}

        detector_rst_c = Signal()
        align_cnt = Signal(3)
        align_c = Signal()
        align_r = Signal()
        align_p = Signal()

        self.comb += align_c.eq(~self.n_align_i)
        self.comb += align_p.eq(~align_c & align_r)
        self.sync += align_r.eq(align_c)

        # fmt: off
        self.sync += [
            If(self.n_align_i,
                detector_rst_c.eq(0),
                If(align_cnt < 5,
                    align_cnt.eq(align_cnt + 1)
                ).Else(
                    align_cnt.eq(1),
                    detector_rst_c.eq(1),
                ),
            ).Else(
                align_cnt.eq(0),
                detector_rst_c.eq(1),
            )
        ]

        self.sync += [
            If(align_p,
                self.align_o.eq(~self.align_o),
            ),
        ]
        # fmt: on

        self.sync += self.detector_rst_o.eq(detector_rst_c)


if __name__ == "__main__":
    aligner = Aligner()
    print(convert(aligner, aligner.ios, name="aligner"))
