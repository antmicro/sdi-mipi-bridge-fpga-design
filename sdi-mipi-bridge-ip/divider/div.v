module div(
	output pix_clk,
	input sys_clk,
	input n_rst,
	input mode_i

	  );

wire sys_rst;
wire mode_c;
reg mode_r = 1'd0;
wire mode_p;
reg sys_div_r = 1'd0;

assign mode_c = (~mode_i);
assign mode_p = (mode_c ^ mode_r);
assign pix_clk = sys_div_r;
assign sys_rst = (~n_rst);

always @(posedge sys_clk) begin
	mode_r <= mode_c;
	if (mode_p) begin
		sys_div_r <= sys_div_r;
	end else begin
		sys_div_r <= (~sys_div_r);
	end
	if (sys_rst) begin
		mode_r <= 1'd0;
		sys_div_r <= 1'd0;
	end
end

endmodule
