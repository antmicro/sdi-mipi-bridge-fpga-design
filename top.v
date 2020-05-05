//Internal clock
module OSCI (HFOUTEN, HFCLKOUT,LFCLKOUT);
parameter HFCLKDIV = 1;
input HFOUTEN;
input HFCLKOUT;
output LFCLKOUT;
endmodule


module top (
     output led,
	 output csi2_inst_tinit_done_o,
	 input  csi2_inst_pix_clk_i,
	 input  csi2_inst_reset_n_i, 
	 input [7:0] csi2_inst_data_i,
	 input csi2_inst_hsync,
	 input csi2_inst_vsync,
	 output csi2_inst_pll_lock_o
	 
);

wire [23:0]data_oi;
assign csi2_inst_dvalid_i = lv_oi;
assign csi2_inst_pd_dphy_i = 1'b0;
wire [23:0]data;

assign data[7:0]  = csi2_inst_data_i[7:0];


//CMOS2DPHY IP core instance
csi2_inst I2 (.pixdata_d0_i({data}), .clk_n_o(csi2_inst_clk_n_o), 
            .clk_p_o(csi2_inst_clk_p_o), .d0_n_io(csi2_inst_d0_n_io), .d0_p_io(csi2_inst_d0_p_io), 
            .d1_n_o(csi2_inst_d1_n_o), .d1_p_o(csi2_inst_d1_p_o), .dvalid_i(csi2_inst_dvalid_i), 
            .fv_i(fv_oi), .lv_i(lv_oi), .pd_dphy_i(csi2_inst_pd_dphy_i), 
            .pix_clk_i(csi2_inst_pix_clk_i), .pll_lock_o(csi2_inst_pll_lock_o), 
            .reset_n_i(csi2_inst_reset_n_i), .tinit_done_o(csi2_inst_tinit_done_o));


// RGB patern generator instance (1280 x 720 p @ 60 Hz)
csi2_inst_pattern_gen I4(.sys_rst(csi2_inst_reset_n_i), .sys_clk(csi2_inst_pix_clk_i),
			 .vsync_i(csi2_inst_vsync), .hsync_i(csi2_inst_hsync), .de_o(de_oi), .data_o({data_oi}), .fv_o(fv_oi), 
			.lv_o(lv_oi));
			
			
defparam I1.HFCLKDIV = 2; // 1,2,4,8

OSCI I1 (.HFOUTEN(1'b1),.HFCLKOUT(HFCLKOUT),.LFCLKOUT(LFCLKOUT));  //internal 48 MHz clock instance
    
	
	
/* heartbeat LED blinking with 1 Hz frequency */
reg [24:0]counter = 0;
reg led_counter;
always @(posedge HFCLKOUT) begin
counter <= counter + 1;

if (counter > 24000000) begin 
	counter <= 0;
    led_counter <= !led_counter;    

 end
 end
 
 assign led = led_counter;
 
endmodule




















