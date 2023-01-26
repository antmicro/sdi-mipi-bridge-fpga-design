// Internal clock
module OSCI (HFOUTEN, HFCLKOUT,LFCLKOUT);
parameter HFCLKDIV = 1;
input HFOUTEN;
input HFCLKOUT;
output LFCLKOUT;
endmodule

module top (
	input  csi2_inst_pix_clk_i,
	output  csi2_inst_reset_n_o,
	input [7:0] csi2_inst_data_i,
	input csi2_inst_hsync,
	input csi2_inst_vsync,
	output csi2_inst_pll_lock_o,
	output csi2_inst_tinit_done_o,
	output led
);

assign csi2_inst_dvalid_i = lv_oi;
assign csi2_inst_pd_dphy_i = 1'b0;

// Heartbeat LED blinking with 1 Hz frequency and deserializer reset
reg [24:0]counter = 0;
reg led_counter;
reg rst_n = 0;

// CMOS2DPHY IP core instance
csi2_inst I2 (
	.pixdata_d0_i({csi2_inst_data_i}),
	.clk_n_o(csi2_inst_clk_n_o),
	.clk_p_o(csi2_inst_clk_p_o),
	.d0_n_io(csi2_inst_d0_n_io),
	.d0_p_io(csi2_inst_d0_p_io),
	.d1_n_o(csi2_inst_d1_n_o),
	.d1_p_o(csi2_inst_d1_p_o),
	.dvalid_i(csi2_inst_dvalid_i),
	.fv_i(fv_oi),
	.lv_i(lv_oi),
	.pd_dphy_i(csi2_inst_pd_dphy_i),
	.pix_clk_i(csi2_inst_pix_clk_i),
	.pll_lock_o(csi2_inst_pll_lock_o),
	.reset_n_i(csi2_inst_reset_n_o),
	.tinit_done_o(csi2_inst_tinit_done_o)
);

// Timing and synchronization module instance (1280 x 720 p @ 60 Hz)
sdi2mipi I4(
	.n_rst(csi2_inst_reset_n_o),
	.sys_clk(csi2_inst_pix_clk_i),
	.vsync_i(csi2_inst_vsync),
	.hsync_i(csi2_inst_hsync),
	.fv_o(fv_oi),
	.lv_o(lv_oi),
	.data_i(csi2_inst_data_i)
);
// Internal 48 MHz clock instance
defparam I1.HFCLKDIV = 2;			// 1,2,4,8
OSCI I1 (
	.HFOUTEN(1'b1),
	.HFCLKOUT(HFCLKOUT),
	.LFCLKOUT(LFCLKOUT)
);

always @(posedge HFCLKOUT) begin
	counter <= counter + 1;

	if (counter > 24000000) begin
		counter <= 0;
		led_counter <= !led_counter;
		if (~rst_n) begin
			rst_n <= !rst_n;
		end
	end
end

assign led = led_counter;
// Drive the reset inout port
assign csi2_inst_reset_n_o = rst_n;

endmodule
