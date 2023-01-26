#!/usr/bin/env python3

from migen import *
from migen.fhdl.verilog import convert

from sdi2mipi import SDI2MIPI


class Top(Module):
    def __init__(self, instance=False):
        self.clock_domains.sys = ClockDomain("sys")
        self.clock_domains.hfc = ClockDomain("hfc")

        # IOs

        self.csi2_inst_pix_clk_i = Signal()
        self.csi2_inst_reset_n_o = Signal()

        self.csi2_inst_data_i = Signal(8)
        self.csi2_inst_hsync = Signal()
        self.csi2_inst_vsync = Signal()
        self.csi2_inst_clk_n_o = Signal()
        self.csi2_inst_clk_p_o = Signal()
        self.csi2_inst_d0_n_io = Signal()
        self.csi2_inst_d0_p_io = Signal()
        self.csi2_inst_d1_n_o = Signal()
        self.csi2_inst_d1_p_o = Signal()
        self.csi2_inst_pll_lock_o = Signal()
        self.csi2_inst_tinit_done_o = Signal()

        self.led = Signal()
        self.hfclkout = Signal()
        self.lfclkout = Signal()

        self.ios = {
            self.csi2_inst_pix_clk_i,
            self.csi2_inst_reset_n_o,
            self.csi2_inst_data_i,
            self.csi2_inst_hsync,
            self.csi2_inst_vsync,
            self.csi2_inst_clk_n_o,
            self.csi2_inst_clk_p_o,
            self.csi2_inst_d0_n_io,
            self.csi2_inst_d0_p_io,
            self.csi2_inst_d1_n_o,
            self.csi2_inst_d1_p_o,
            self.csi2_inst_pll_lock_o,
            self.csi2_inst_tinit_done_o,
            self.led,
            self.hfclkout,
            self.lfclkout,
        }

        # Logic (clk & rst)

        n_rst = Signal()
        self.comb += [
            self.sys.clk.eq(self.csi2_inst_pix_clk_i),
            self.sys.rst.eq(~n_rst),
        ]

        self.comb += [self.hfc.clk.eq(self.hfclkout), self.hfc.rst.eq(~n_rst)]

        # Logic (other)

        self.comb += self.csi2_inst_reset_n_o.eq(~n_rst)

        fv_oi = Signal()
        lv_oi = Signal()
        csi2_inst_dvalid_i = Signal()
        csi2_inst_pd_dphy_i = Signal()

        self.comb += [csi2_inst_dvalid_i.eq(lv_oi), csi2_inst_pd_dphy_i.eq(0)]

        self.specials += Instance(
            "csi2_inst",
            i_pixdata_d0_i=self.csi2_inst_data_i,
            i_dvalid_i=csi2_inst_dvalid_i,
            i_fv_i=fv_oi,
            i_lv_i=lv_oi,
            i_pd_dphy_i=csi2_inst_pd_dphy_i,
            i_pix_clk_i=self.csi2_inst_pix_clk_i,
            i_reset_n_i=n_rst,
            io_clk_n_o=self.csi2_inst_clk_n_o,
            io_clk_p_o=self.csi2_inst_clk_p_o,
            io_d0_n_io=self.csi2_inst_d0_n_io,
            io_d0_p_io=self.csi2_inst_d0_p_io,
            io_d1_n_o=self.csi2_inst_d1_n_o,
            io_d1_p_o=self.csi2_inst_d1_p_o,
            o_pll_lock_o=self.csi2_inst_pll_lock_o,
            o_tinit_done_o=self.csi2_inst_tinit_done_o,
        )

        if instance:
            self.specials += Instance(
                "sdi2mipi",
                i_n_rst=n_rst,
                i_sys_clk=self.csi2_inst_pix_clk_i,
                i_vsync_i=self.csi2_inst_vsync,
                i_hsync_i=self.csi2_inst_hsync,
                i_data_i=self.csi2_inst_data_i,
                o_fv_o=fv_oi,
                o_lv_o=lv_oi,
            )
        else:
            self.submodules.sdi2mipi = SDI2MIPI(video_format="720p60", four_lanes=False)
            self.comb += [
                self.sdi2mipi.vsync_i.eq(self.csi2_inst_vsync),
                self.sdi2mipi.hsync_i.eq(self.csi2_inst_hsync),
                self.sdi2mipi.data_i.eq(self.csi2_inst_data_i),
                fv_oi.eq(self.sdi2mipi.fv_o),
                lv_oi.eq(self.sdi2mipi.lv_o),
            ]

        self.specials += Instance(
            "OSCI",
            p_HFCLKDIV=2,
            i_HFOUTEN=1,
            o_HFCLKOUT=self.hfclkout,
            o_LFCLKOUT=self.lfclkout,
        )

        MAX_COUNTER = 24000000
        counter = Signal(max=MAX_COUNTER)

        self.sync.hfc += [
            counter.eq(counter + 1),
            # fmt: off
            If(counter == MAX_COUNTER,
                self.led.eq(~self.led),
                If(~n_rst, n_rst.eq(~n_rst)),
            ),
            # fmt: on
        ]


if __name__ == "__main__":
    top = Top()
    print(convert(top, top.ios, name="top"))
