`timescale 1ns/10ps

module iver_tb;

	parameter integer HA = 1280;
	parameter integer HS = 40;
	parameter integer HBP = 220;
	parameter integer HFP = 110;
	parameter integer VA = 720;
	parameter integer VS = 5;
	parameter integer VBP = 20;
	parameter integer VFP = 5;

	parameter integer FRAMES = 5;
	parameter integer PER = 14;
	parameter integer MUL = 2;
	parameter integer H_ACTIVE = HA * PER * MUL;
	parameter integer H_SYNC = HS * PER * MUL;
	parameter integer H_BACK_PORCH = HBP * PER * MUL;
	parameter integer H_FRONT_PORCH = HFP * PER * MUL;
	parameter integer H_TOTAL = H_ACTIVE + H_SYNC + H_BACK_PORCH + H_FRONT_PORCH;
	parameter integer H_NO_SYNC = H_ACTIVE + H_BACK_PORCH + H_FRONT_PORCH;
	parameter integer V_ACTIVE = VA;
	parameter integer V_SYNC = VS;
	parameter integer V_BACK_PORCH = VBP;
	parameter integer V_FRONT_PORCH = VFP;
	parameter integer V_TOTAL = V_ACTIVE + V_SYNC + V_BACK_PORCH + V_FRONT_PORCH;

	integer i;
	integer k;
	integer j;

	reg sys_clk = 0;
	reg reset = 0;
	reg n_align_i = 0;
	wire align_o;
	wire detector_rst_o;


	initial begin
		$dumpfile("align.vcd");
		$dumpvars(0, iver_tb);
		#(50*PER*MUL) reset = 0;
		#(50*PER*MUL)
		#(50*PER*MUL) reset = 1;
		#(50*PER*MUL) reset = 0;
		#(500*PER*MUL) n_align_i = 1;
		#(5*PER*MUL) n_align_i = 0;
		#(500*PER*MUL)
		#1 $finish;
	end

	always #(PER*MUL/4) sys_clk = !sys_clk;

	aligner UUT (
		.sys_clk(sys_clk),
		.sys_rst(reset),
		.n_align_i(n_align_i),
		.align_o(align_o),
		.detector_rst_o(detector_rst_o)
		);
endmodule
