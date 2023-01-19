from migen import *

class TimingGenerator(Module):
    def __init__(self, timings):

        # VESA timing parameters
        H_ACTIVE        =  timings["H_ACTIVE"]
        H_TOTAL         =  timings["H_TOTAL"]
        V_ACTIVE        =  timings["V_ACTIVE"]
        V_TOTAL         =  timings["V_TOTAL"]
        H_SYNC          =  timings["H_SYNC"]
        H_BACK_PORCH    =  timings["H_BACK_PORCH"]
        H_FRONT_PORCH   =  timings["H_FRONT_PORCH"]
        V_SYNC          =  timings["V_SYNC"]
        V_BACK_PORCH    =  timings["V_BACK_PORCH"]
        V_FRONT_PORCH   =  timings["V_FRONT_PORCH"]

        # Sys clock divided by 2
        # effectively a pixel clock compliant with VESA timings
        self.clock_domains.pix = ClockDomain(name="pix")

        # Inputs
        self.vsync_i = Signal()
        self.hsync_i = Signal()
        self.n_rst = Signal()

        # Outputs
        self.fv_o = Signal()
        self.lv_o = Signal()

        # Input/Output list for correct module generation
        self.ios = {self.vsync_i, self.hsync_i,
                    self.fv_o, self.lv_o,
                    self.pix.clk, self.n_rst}

        self.vsync_r = Signal()
        self.vsync_rr = Signal()
        self.hsync_r = Signal()
        self.hsync_rr = Signal()
        self.fv_c = Signal()
        self.lv_c = Signal()
        self.lv_r = Signal()
        self.fv_extend_cnt_c = Signal(10)
        self.fv_extend_cnt_r = Signal(10)
        self.pixcnt_c = Signal(12)
        self.pixcnt_r = Signal(12)
        self.linecnt_c = Signal(12)
        self.linecnt_r = Signal(12)

        # Helper variables
        H_BLANKING = H_BACK_PORCH + H_FRONT_PORCH + H_SYNC
        V_SYNC_START = V_ACTIVE + V_FRONT_PORCH + 1

        ###

        # Convert active-low to active-high reset and distribute it across clock domains
        self.comb += self.pix.rst.eq(~self.n_rst)

        # Signals controled in pixel clock domain
        self.sync.pix += [
                self.vsync_r.eq(self.vsync_i),
                self.vsync_rr.eq(self.vsync_r),
                self.hsync_r.eq(self.hsync_i),
                self.hsync_rr.eq(self.hsync_r),
                self.fv_o.eq(self.fv_c),
                self.lv_r.eq(self.lv_c),
                self.lv_o.eq((self.lv_r) & self.fv_o),
                self.pixcnt_r.eq(self.pixcnt_c),
                self.linecnt_r.eq(self.linecnt_c),
                self.fv_extend_cnt_r.eq(self.fv_extend_cnt_c),
        ]

        # Pixel counter
        self.comb += [
            If (self.hsync_r & ~self.hsync_rr,
                self.pixcnt_c.eq(H_ACTIVE + H_FRONT_PORCH + 1),
            ).Else (
                If (self.pixcnt_r < H_TOTAL,
                    self.pixcnt_c.eq(self.pixcnt_r + 1)
                ).Else (
                    self.pixcnt_c.eq(1)
                )
            )
        ]

        # Line_valid generation
        self.comb += self.lv_c.eq((self.pixcnt_r > 0) & (self.pixcnt_r <= H_ACTIVE))

        # Line counter
        self.comb += [
            If (self.vsync_r & ~self.vsync_rr,
                    self.linecnt_c.eq(V_SYNC_START)
            ).Elif ((self.linecnt_r < V_TOTAL) & (self.pixcnt_r == 1),
                self.linecnt_c.eq(self.linecnt_r + 1)
            ).Elif ((self.linecnt_r == V_TOTAL) & (self.pixcnt_r == 1),
                self.linecnt_c.eq(1)
            ).Else (
                self.linecnt_c.eq(self.linecnt_r)
            )
        ]

        # Frame_valid generation
        self.comb += self.fv_c.eq((self.linecnt_r > 0) & (self.linecnt_r <= V_ACTIVE) | ((self.fv_extend_cnt_r > 0)))

        # Extend frame_valid signal by one horizontal blanking period
        self.comb += [
            If ((self.linecnt_r == V_TOTAL) & (self.pixcnt_r >= H_ACTIVE),
                self.fv_extend_cnt_c.eq(self.fv_extend_cnt_r + 1),
            ).Else (
                self.fv_extend_cnt_c.eq(0)
            )
        ]
