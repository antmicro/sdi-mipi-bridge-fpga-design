`timescale 1ps/1ps

module iver_tb;

	parameter integer H_ACTIVE = 1280;
	parameter integer H_SYNC = 40;
	parameter integer H_BACK_PORCH = 220;
	parameter integer H_FRONT_PORCH = 110;
	parameter integer V_ACTIVE = 720;
	parameter integer V_SYNC = 5;
	parameter integer V_BACK_PORCH = 20;
	parameter integer V_FRONT_PORCH = 5;

	parameter integer FRAMES = 3;
	parameter integer PER = 13468;
	parameter integer MUL = 1;

	parameter integer HA = H_ACTIVE * PER * MUL;
	parameter integer HS = H_SYNC * PER * MUL;
	parameter integer HBP = H_BACK_PORCH * PER * MUL;
	parameter integer HFP = H_FRONT_PORCH * PER * MUL;
	parameter integer H_TOTAL = HA + HS + HBP + HFP;
	parameter integer H_NO_SYNC = HA + HBP + HFP;
	parameter integer V_TOTAL = V_ACTIVE + V_SYNC + V_BACK_PORCH + V_FRONT_PORCH;

	integer i;
	integer k;
	integer j;

	reg reset = 1;
	reg vsync;
	reg hsync;
	wire fv_o;
	wire lv_o;

	initial begin
		$dumpfile("timing.vcd");
		$dumpvars(0, iver_tb);
		#5000
		#50 reset = 1;
		#50 reset = 0;
		#5000
		for (i = 0; i < FRAMES; i = i + 1) begin
			vsync = 1;
			for (k = 0; k < V_SYNC; k = k + 1) begin
				hsync = 1;
				#HS hsync = 0;
				#H_NO_SYNC;
			end
			vsync = 0;
			for (k = 0; k < V_TOTAL - V_SYNC; k = k + 1) begin
				hsync = 1;
				#HS hsync = 0;
				#H_NO_SYNC;
			end
		end
		#1 $finish;
	end

	reg clk = 0;
	always #(PER/2) clk = !clk;

	timing_gen UUT (
		.pix_clk(clk),
		.pix_rst(reset),
		.vsync_i(vsync),
		.hsync_i(hsync),
		.fv_o(fv_o),
		.lv_o(lv_o));
endmodule
