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


from migen import *
from migen.fhdl.verilog import convert


class Top(Module):
    def __init__(self, four_lanes=False):
        self.clock_domains.sys = ClockDomain("sys")
        self.clock_domains.hfc = ClockDomain("hfc")

        # IOs
        common_ios = {
            "i_pixdata_d0_i": Signal(8, name="deserializer_data_i"),
            "i_pix_clk_i": Signal(name="deserializer_pix_clk_i"),
            "io_clk_n_o": Signal(name="mipi_dphy_clk_n_o"),
            "io_clk_p_o": Signal(name="mipi_dphy_clk_p_o"),
            "io_d0_n_io": Signal(name="mipi_dphy_d0_n_io"),
            "io_d0_p_io": Signal(name="mipi_dphy_d0_p_io"),
            "io_d1_n_o": Signal(name="mipi_dphy_d1_n_o"),
            "io_d1_p_o": Signal(name="mipi_dphy_d1_p_o"),
        }
        ext_ios = {
            "user_led": Signal(name="user_led"),
            "cdone_led": Signal(name="cdone_led"),
            "i_vblank_i": Signal(name="deserializer_vblank_i"),
            "i_hblank_i": Signal(name="deserializer_hblank_i"),
            "des_reset_n": Signal(name="des_reset_n"),
        }
        self.ios = set(dict(**common_ios, **ext_ios).values())

        base_csi2_inst_signals = {
            "i_reset_n_i": Signal(name="csi2_inst_reset_n_io"),
            "o_tinit_done_o": Signal(name="csi2_inst_tinit_done_o"),
            "o_pll_lock_o": Signal(name="csi2_inst_pll_lock_o"),
            "i_pd_dphy_i": Signal(name="csi2_inst_pd_dphy_i"),
            "i_dvalid_i": Signal(name="csi2_inst_dvalid_i"),
            "i_fv_i": Signal(name="fv_oi"),
            "i_lv_i": Signal(name="lv_oi"),
        }

        # Logic (clk & rst)
        csi2_inst_pix_clk_i = common_ios["i_pix_clk_i"]
        hfclkout = Signal(name="hfclkout")
        lfclkout = Signal(name="lfclkout")
        des_reset_n = ext_ios["des_reset_n"]
        rst_n = base_csi2_inst_signals["i_reset_n_i"]
        self.comb += [
            self.sys.clk.eq(csi2_inst_pix_clk_i),
            self.sys.rst.eq(~rst_n),
            self.hfc.clk.eq(hfclkout),
        ]

        # Logic (other)
        user_led = ext_ios["user_led"]
        tinit_done = base_csi2_inst_signals["o_tinit_done_o"]
        fv_oi = base_csi2_inst_signals["i_fv_i"]
        lv_oi = base_csi2_inst_signals["i_lv_i"]
        csi2_inst_dvalid_i = base_csi2_inst_signals["i_dvalid_i"]
        csi2_inst_pd_dphy_i = base_csi2_inst_signals["i_pd_dphy_i"]

        # fmt: off
        self.comb += [
            csi2_inst_dvalid_i.eq(lv_oi),
            csi2_inst_pd_dphy_i.eq(0),
            user_led.eq(tinit_done),
        ]
        # fmt: on

        base_csi2_inst_ios = dict(**common_ios, **base_csi2_inst_signals)
        if four_lanes:
            ext_csi2_inst_signals = {
                "io_d2_n_o": Signal(name="mipi_dphy_d2_n_o"),
                "io_d2_p_o": Signal(name="mipi_dphy_d2_p_o"),
                "io_d3_n_o": Signal(name="mipi_dphy_d3_n_o"),
                "io_d3_p_o": Signal(name="mipi_dphy_d3_p_o"),
            }
            self.ios.update(ext_csi2_inst_signals.values())
            ext_csi2_inst_ios = dict(**base_csi2_inst_ios, **ext_csi2_inst_signals)
            self.specials += Instance("csi2_inst", **ext_csi2_inst_ios)
        else:
            self.specials += Instance("csi2_inst", **base_csi2_inst_ios)

        vblank = ext_ios["i_vblank_i"]
        hblank = ext_ios["i_hblank_i"]

        vblank_d = Signal()
        fv_ext = Signal()
        self.comb += [
            fv_oi.eq(~vblank | ~vblank_d | fv_ext),
            lv_oi.eq(~hblank & ~vblank),
        ]

        # fmt: off
        self.specials += Instance(
            "OSCI",
            p_HFCLKDIV = 2,
            i_HFOUTEN  = 1,
            o_HFCLKOUT = hfclkout,
            o_LFCLKOUT = lfclkout,
        )
        # fmt: on

        COUNTER_1s = 24000000
        COUNTER_100ms = COUNTER_1s // 10
        COUNTER_100us = COUNTER_100ms // 1000
        counter = Signal(max=COUNTER_1s)
        cdone_led = ext_ios["cdone_led"]

        self.sync.hfc += [
            # fmt: off
            counter.eq(counter + 1),
            If(counter > COUNTER_100ms,
                If(~des_reset_n,
                    des_reset_n.eq(1),
                ),
            ),
            If(counter > COUNTER_1s,
                counter.eq(0),
                cdone_led.eq(~cdone_led),
                If(~rst_n,
                    rst_n.eq(1),
                ),
            ),
            # fmt: on
        ]

        # Add a delay between vblank and hblank timings
        fv_cnt = Signal(max=COUNTER_100us)
        self.sync += [
            # fmt: off
            vblank_d.eq(vblank),
            If((vblank ^ vblank_d),
                fv_cnt.eq(COUNTER_100us),
                fv_ext.eq(1),
            ).Elif(fv_cnt == 0,
                fv_cnt.eq(0),
                fv_ext.eq(0),
            ).Else(
                fv_cnt.eq(fv_cnt - 1),
                fv_ext.eq(1),
            )
            # fmt: on
        ]


if __name__ == "__main__":
    top = Top()
    print(convert(top, top.ios, name="top"))
