from migen.fhdl.verilog import convert
from migen import *

class DetectTRS(Module):
    def __init__(self):

        self.data_i = Signal(8)
        self.n_rst = Signal()
        self.lv_i = Signal()
        self.n_align_o = Signal()

        # Input clock from deserializer
        # doubled pixel clock frequency for given resolution
        self.clock_domains.sys = ClockDomain(name="sys")

        self.comb += self.sys.rst.eq(~self.n_rst)

        # Sys clock divided by 2
        # effectively a pixel clock compliant with VESA timings
        self.clock_domains.pix = ClockDomain(name="pix")

        # Input/Output list for correct module generation
        self.ios = {self.sys.clk, self.pix.clk, self.n_rst,
                    self.data_i, self.lv_i, self.n_align_o}

        # Flags for checking word alignment
        F1 = Signal()
        F2 = Signal()
        F3 = Signal()

        detect_trs = Signal()
        s1 = Signal()
        s2 = Signal(2)
        s3 = Signal()

        # Detect EAV preamble: 0xFF 0xFF 0x0 0x0 0x0 0x0 0xB6 0xB6
        detect = FSM(reset_state="FIRST_OK")
        self.submodules += detect
        detect_trs.eq(detect.ongoing("DONE"))

        detect.act("FIRST_OK",
            detect_trs.eq(0),
            If (~self.lv_i,
                If (self.data_i == 0xFF,
                    If (s1 < 1,
                        NextValue(s1, s1 + 1),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("FIRST_OK"),
                    ).Else (
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("SECOND_OK"),
                        If (self.pix.clk,
                            NextValue(F1, 1),
                        ).Else (
                            NextValue(F1, 0),
                        )
                    )
                ).Else (
                    NextValue(s1, 0),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                )
            ).Else (
                NextValue(s1, 0),
                NextValue(s2, 0),
                NextValue(s3, 0),
                NextState("FIRST_OK"),
            )
        )

        detect.act("SECOND_OK",
            detect_trs.eq(0),
            If (~self.lv_i,
                If (self.data_i == 0x0,
                    If (s2 < 3,
                        NextValue(s1, 0),
                        NextValue(s2, s2 + 1),
                        NextValue(s3, 0),
                        NextState("SECOND_OK"),
                    ).Else (
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("THIRD_OK"),
                        If (self.pix.clk,
                            NextValue(F2, 1),
                        ).Else (
                            NextValue(F2, 0),
                        )
                    )
                ).Elif (self.data_i == 0xFF,
                    NextValue(s1, 1),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ).Else (
                    NextValue(s1, 0),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                )
            ).Else (
                NextValue(s1, 0),
                NextValue(s2, 0),
                NextValue(s3, 0),
                NextState("FIRST_OK"),
            )
        )

        detect.act("THIRD_OK",
            detect_trs.eq(0),
            If (~self.lv_i,
                # Detect XY byte for EAV in vertical blanking: 0xB6
                If ((self.data_i & 0xF0) == 0xB0,
                    If (s3 < 1,
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, s3 + 1),
                        NextState("THIRD_OK"),
                    ).Else (
                        NextValue(s1, 0),
                        NextValue(s2, 0),
                        NextValue(s3, 0),
                        NextState("DONE"),
                        If (self.pix.clk,
                            NextValue(F3, 1),
                        ).Else (
                            NextValue(F3, 0),
                        )
                    )
                ).Elif (self.data_i == 0xFF,
                    NextValue(s1, 1),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                ).Else (
                    NextValue(s1, 0),
                    NextValue(s2, 0),
                    NextValue(s3, 0),
                    NextState("FIRST_OK"),
                )
            ).Else (
                NextValue(s1, 0),
                NextValue(s2, 0),
                NextValue(s3, 0),
                NextState("FIRST_OK"),
            )
        )

        detect.act("DONE",
            detect_trs.eq(1),
        )

        # Check alignment
        self.sync += [
            If (detect_trs & F1 & F2 & F3,
                self.n_align_o.eq(1)
            )
        ]

if __name__ == "__main__":
    detect = DetectTRS()
    convert(detect, detect.ios, name="detector").write("detector.v")
