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


from migen.fhdl.structure import *
from migen.fhdl.module import Module
from migen.fhdl import verilog


class Divider(Module):
    """
    A module that is responsible for preparing pixel clock in 720p setup from
    deserializer clock output and creating one input clock delay.
    """

    def __init__(self):

        # IO signals

        self.rst_i = ResetSignal()
        self.clk_i = ClockSignal()
        self.mode_i = Signal()
        self.pix_clk_o = Signal()

        self.ios = {self.mode_i, self.pix_clk_o}

        # logic

        mode_c = Signal()
        mode_r = Signal()
        mode_p = Signal()
        sys_div_r = Signal()

        self.comb += [
            mode_c.eq(~self.mode_i),
            mode_p.eq(mode_c ^ mode_r),
            self.pix_clk_o.eq(sys_div_r),
        ]

        self.sync += [
            mode_r.eq(mode_c),
            # fmt: off
            If(mode_p,
                sys_div_r.eq(sys_div_r),
            ).Else(
                sys_div_r.eq(~sys_div_r),
            ),
            # fmt: on
        ]


if __name__ == "__main__":
    divider = Divider()
    print(verilog.convert(divider, divider.ios, name="divider"))
