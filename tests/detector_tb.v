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
	reg pix_clk = 0;
	reg reset = 1;
	reg lv = 0;
	reg [7:0] data;

	initial begin
		$dumpfile("detector.vcd");
		$dumpvars(0, iver_tb);
		lv = 0;
		#(5000*PER*MUL)
		#(50*PER*MUL) reset = 1;
		#(50*PER*MUL) reset = 0;
		#(5000*PER*MUL)
		for (i = 0; i < FRAMES; i = i + 1) begin
			lv = 0;
			#(V_TOTAL - V_ACTIVE);
			for (k = 0; k < V_ACTIVE; k = k + 1) begin
				#(((H_TOTAL-H_ACTIVE)/2)-(3*PER*MUL)) data = 8'h0;
				reset = 1;
				#(50*PER*MUL) reset = 0;
				#(50*PER*MUL)
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hde;
				#(PER) data = 8'h0;
				#(PER) data = 8'hbc;
				#(PER) data = 8'haf;
				#(PER) data = 8'h0;
				#(PER) data = 8'hbc;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'hB6;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h80;
				#(PER) data = 8'h80;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h9D;
				#(PER) data = 8'h9D;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hAB;
				#(PER) data = 8'hAB;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hB6;
				#(PER) data = 8'hB6;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hC7;
				#(PER) data = 8'hC7;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hDA;
				#(PER) data = 8'hDA;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hEC;
				#(PER) data = 8'hEC;

				#(PER) data = 8'hff;
				#(PER) data = 8'hff;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'h0;
				#(PER) data = 8'hF1;
				#(PER) data = 8'hF1;

				#(PER) data = 8'h0;
				#((H_TOTAL-H_ACTIVE)/2) lv = 1;
				#H_ACTIVE lv = 0;
			end
		end
		#1 $finish;
	end

	always #(PER*MUL/4) sys_clk = !sys_clk;
	always #(PER*MUL/2) pix_clk = !pix_clk;

	detector UUT (
		.det_clk(sys_clk),
		.det_rst(reset),
		.pix_clk(pix_clk),
		.lv_i(lv),
		.data_i(data));
endmodule
