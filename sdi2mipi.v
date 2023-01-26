module CLKDIVG (RST, CLKI, ALIGNWD, CDIVX);
	parameter DIV = "2.0";
	parameter GSR = "DISABLED";
	input RST, CLKI, ALIGNWD;
	output CDIVX;
endmodule

module sdi2mipi(
	input sys_clk,
	input n_rst,
	input vsync_i,
	input hsync_i,
	input [7:0]data_i,
	output fv_o,
	output lv_o);

wire pix_clk;

CLKDIVG I1 (
	.RST(~n_rst),
	.CLKI(sys_clk),
	.ALIGNWD(align_sig),
	.CDIVX(pix_clk));

timing_gen gen(
	.pix_clk(pix_clk),
	.n_rst(n_rst),
	.vsync_i(vsync_i),
	.hsync_i(hsync_i),
	.fv_o(fv_o),
	.lv_o(lv_o));

detector detect(
	.data_i(data_i),
	.n_rst(detector_rst),
	.lv_i(lv_o),
	.n_align_o(n_align_o),
	.sys_clk(sys_clk),
	.pix_clk(pix_clk));

aligner align(
	.n_rst(n_rst),
	.n_align_i(n_align_o),
	.detector_rst_o(detector_rst),
	.align_o(align_sig),
	.sys_clk(sys_clk));

endmodule
