from migen.fhdl.verilog import convert
from migen import *

class Aligner(Module):
    def __init__(self):

        self.n_rst = Signal()
        self.n_align_i = Signal()
        self.detector_rst_o = Signal()
        self.align_o = Signal()

        # Input clock from deserializer
        # doubled pixel clock frequency for given resolution
        self.clock_domains.sys = ClockDomain(name="sys")

        self.comb += self.sys.rst.eq(~self.n_rst)

        # Input/Output list for correct module generation
        self.ios = {self.sys.clk, self.n_rst,
                    self.n_align_i,
                    self.align_o, self.detector_rst_o}

        detector_rst_c = Signal()
        align_cnt = Signal(3)
        align_c = Signal()
        align_r = Signal()
        align_p = Signal()

        self.comb += align_c.eq(~self.n_align_i)
        self.comb += align_p.eq(~align_c & align_r)
        self.sync += align_r.eq(align_c)

        self.sync += [
            If (self.n_align_i,
                detector_rst_c.eq(0),
                If (align_cnt < 5,
                    align_cnt.eq(align_cnt + 1)
                ).Else (
                    align_cnt.eq(1),
                    detector_rst_c.eq(1),
                )
            ).Else (
                align_cnt.eq(0),
                detector_rst_c.eq(1),
            )
        ]

        self.sync += [
            If (align_p,
                self.align_o.eq(~self.align_o),
            )
        ]

        self.sync += [
            self.detector_rst_o.eq(detector_rst_c),
        ]

if __name__ == "__main__":
    aligner = Aligner()
    convert(aligner, aligner.ios, name="aligner").write("aligner.v")
