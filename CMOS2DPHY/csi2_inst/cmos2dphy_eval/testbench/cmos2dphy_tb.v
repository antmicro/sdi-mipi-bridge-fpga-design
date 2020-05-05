//===========================================================================
// Filename: cmos2dphy_tb.v
// Copyright(c) 2016 Lattice Semiconductor Corporation. All rights reserved. 
//===========================================================================
`timescale 1ps / 10fs

`ifdef TX_CSI2

`include "cmos_model.v"

module top(); 
`ifndef NUM_FRAMES
   parameter num_frames = 1;
`else
   parameter num_frames = `NUM_FRAMES;
`endif

`ifndef NUM_LINES
   parameter num_lines  = 4;
`else
   parameter num_lines  = `NUM_LINES;
`endif

`ifndef NUM_PIXELS
   parameter num_pixels = 1000;
`else 
   parameter num_pixels = `NUM_PIXELS;
`endif

   parameter refclk_period = `PIX_CLK;

`ifndef INIT_DRIVE_DELAY
   parameter init_drive_delay     = 100000;
`else
   parameter init_drive_delay     = `INIT_DRIVE_DELAY;
`endif

// timing related parameters
`ifndef FV_H_TO_LV_H
   parameter cmos_fv_h_to_lv_h          = 800;
`else
   parameter cmos_fv_h_to_lv_h          = `FV_H_TO_LV_H;
`endif

`ifndef LV_L_TO_LV_H
   parameter cmos_lv_l_to_lv_h          = 800;
`else
   parameter cmos_lv_l_to_lv_h          = `LV_L_TO_LV_H;
`endif

`ifndef LV_L_TO_FV_L
   parameter cmos_lv_l_to_fv_l          = 800;
`else
   parameter cmos_lv_l_to_fv_l          = `LV_L_TO_FV_L;
`endif

`ifndef FV_L_TO_FV_H
   parameter cmos_fv_l_to_fv_h          = 800;
`else
   parameter cmos_fv_l_to_fv_h          = `FV_L_TO_FV_H;
`endif


`ifdef RAW8
   parameter long_even_line_en    = 0;
   parameter dwidth = 8;
`elsif RAW10
   parameter long_even_line_en    = 0;
   parameter dwidth = 10;
`elsif RAW12
   parameter long_even_line_en    = 0;
   parameter dwidth = 12;
`elsif RGB888
   parameter long_even_line_en    = 0;
   parameter dwidth = 24;
`elsif YUV420_10
   parameter long_even_line_en    = 1;
   parameter dwidth = 10;
`elsif YUV420_8
   parameter long_even_line_en    = 1;
   parameter dwidth = 8;
`elsif YUV422_10
   parameter long_even_line_en    = 0;
   parameter dwidth = 10;
`elsif YUV422_8
   parameter long_even_line_en    = 0;
   parameter dwidth = 8;
`endif

   wire refclk_w;
   wire [dwidth - 1 : 0] cmos_data_w;
   wire                  cmos_fv_w;
   wire                  cmos_lv_w;
   reg resetn;
   reg refclk_i;
   wire pll_lock;
   wire tinit_done;
   assign refclk_w = refclk_i;
   reg [31:0] init_delay;

   PUR PUR_INST(resetn);

   cmos_model #(
   .num_frames        (num_frames),
   .num_lines         (num_lines ),  
`ifdef YUV422_10
   .num_pixels        (num_pixels * 2),
`elsif YUV422_8
   .num_pixels        (num_pixels * 2),
`else 
   .num_pixels        (num_pixels),
`endif
   .cmos_fv_h_to_lv_h (cmos_fv_h_to_lv_h),
   .cmos_lv_l_to_lv_h (cmos_lv_l_to_lv_h),
   .cmos_lv_l_to_fv_l (cmos_lv_l_to_fv_l),
   .cmos_fv_l_to_fv_h (cmos_fv_l_to_fv_h),
   .dwidth            (dwidth ),
   .long_even_line_en (long_even_line_en)
      )
   cmos_ch0 (
      .refclk_i  (refclk_w ) ,
      .resetn    (resetn ) ,
      .cmos_data (cmos_data_w ) ,
      .cmos_fv   (cmos_fv_w ) ,
      .cmos_lv   (cmos_lv_w ) 
     );

    SIP7_inst I_rgb_2_dphy(
//------Common Interface Ports
        .pix_clk_i(refclk_w ),        // pixel or refclk clock
        .reset_n_i(resetn ),          // (active low) asynchronous reset
        .pd_dphy_i(0),                // DPHY PD signal

//------Debug Signals available if MISC_ON is defined
`ifdef MISC_ON
        .tinit_done_o(tinit_done),    // Tinit done
        .pll_lock_o  (pll_lock),      // PLL clock lock signal
`endif // MISC_ON

//------CSI Interface Ports
        .fv_i        (cmos_fv_w),     // frame valid input for CMOS i/f
        .lv_i        (cmos_lv_w),     // line valid input for CMOS i/f
        .dvalid_i    (cmos_lv_w),     // data valid
        .pixdata_d0_i(cmos_data_w),   // pixel data for CMOS interface

// DPHY output ports
`ifdef NUM_TX_LANE_1
        .d0_p_io(),       // DPHY output data 0
        .d0_n_io(),       // DPHY output data 0
`elsif NUM_TX_LANE_2
        .d0_p_io(),       //DPHY output data 0
        .d0_n_io(),       //DPHY output data 0
        .d1_p_o (),        //DPHY output data 1
        .d1_n_o (),        //DPHY output data 1
`elsif NUM_TX_LANE_4
        .d0_p_io(),       //DPHY output data 0
        .d0_n_io(),       //DPHY output data 0
        .d1_p_o (),        //DPHY output data 1
        .d1_n_o (),        //DPHY output data 1
        .d2_p_o (),        //DPHY output data 2
        .d2_n_o (),        //DPHY output data 2
        .d3_p_o (),        //DPHY output data 3
        .d3_n_o (),        //DPHY output data 3
`endif // NUM_TX_LANE
        .clk_p_o(),       // DPHY output clock
        .clk_n_o()        // DPHY output clock
     );
   initial begin
      refclk_i = 0;
      resetn = 0;
      init_delay = init_drive_delay;

      $display("%t TEST START\n", $time);
      #(50000);
      resetn = 1;

      `ifdef MISC_ON
         @(posedge tinit_done);
      `endif

      #init_delay;
      
      $display("%t Enabling model\n", $time);
      cmos_ch0.cmos_active = 1;

      @(refclk_i);

      //Waiting to complete model transaction
      @(cmos_ch0.cmos_active == 0);
      #(50000);
      $display("%t TEST END\n", $time);
      $finish;
   end

   initial begin
      $shm_open("./dump.shm");
      $shm_probe(top, ("AC"));
   end

   always #(refclk_period/2) refclk_i =~ refclk_i;

endmodule

`elsif TX_DSI

module top(); 

`ifndef NUM_PIXELS
   parameter total_pix     = 1920;
`else
   parameter total_pix     = `NUM_PIXELS;
`endif

`ifndef NUM_LINES
   parameter total_line    = 2;
`else
   parameter total_line    = `NUM_LINES;
`endif

`ifndef NUM_FRAMES
   parameter num_frames    = 2;
`else
   parameter num_frames    = `NUM_FRAMES;
`endif

`ifndef INIT_DRIVE_DELAY
   parameter init_drive_delay     = 100000;
`else
   parameter init_drive_delay     = `INIT_DRIVE_DELAY;
`endif

`ifndef HFRONT_PORCH
   parameter hfront_porch  = 320;
`else
   parameter hfront_porch  = `HFRONT_PORCH;
`endif

`ifndef HSYNC_PULSE
   parameter hsync_pulse   = 44;
`else
   parameter hsync_pulse   = `HSYNC_PULSE;
`endif

`ifndef HBACK_PORCH
   parameter hback_porch   = 325;
`else
   parameter hback_porch   = `HBACK_PORCH;
`endif

`ifndef VFRONT_PORCH
   parameter vfront_porch  = 4;
`else
   parameter vfront_porch  = `VFRONT_PORCH;
`endif

`ifndef VSYNC_PULSE
   parameter vsync_pulse   = 5;
`else
   parameter vsync_pulse   = `VSYNC_PULSE;
`endif

`ifndef VBACK_PORCH
   parameter vback_porch   = 36;
`else
   parameter vback_porch   = `VBACK_PORCH;
`endif

   parameter refclk_period = `PIX_CLK;

   reg        reset;
   wire       pll_lock;
   wire       dcsrom_done;
   reg        hsync;
   reg        vsync;
   reg        de;
   reg [7:0]  red;
   reg [7:0]  blue;
   reg [7:0]  green;
   wire       clk_lane_dp;
   wire       clk_lane_dn;
   wire [3:0] data_lane_dp;
   wire [3:0] data_lane_dn;
   wire refclk_w;
   wire [23:0] pixdata_d0_i ;

   reg resetn;
   reg refclk_i;
   wire tinit_done;
   assign refclk_w = refclk_i;
   reg [31:0] init_delay;

`ifdef RGB888
   assign pixdata_d0_i[7:0]   = red;
   assign pixdata_d0_i[15:8]  = blue;
   assign pixdata_d0_i[23:16] = green;
`elsif RGB666
   assign pixdata_d0_i[5:0]   = red[5:0];
   assign pixdata_d0_i[11:6]  = blue[5:0];
   assign pixdata_d0_i[17:12] = green[5:0];
`endif

   integer line_cnt  = 0;
   integer frame_cnt = 0;
   integer pixel_cnt = 0;

   initial begin                       
      init_delay = init_drive_delay; 
      resetn     = 1'b0;          
      refclk_i   = 1'b0;
      hsync      = 1'b0;
      vsync      = 1'b0;
      de         = 1'b0;
      red        = 'b0;
      blue       = 'b0;
      green      = 'b0;

      $display("%0t TEST START\n",$time);
 
      #(50000);  
      resetn     = 1'b1;

`ifdef MISC_ON
      @(posedge dcsrom_done);
      $display("%t : dcsrom_done signal has asserted!\n", $time);
`else
      #init_delay;
`endif

      @(negedge refclk_i);

      repeat (num_frames) begin

         frame_cnt = frame_cnt + 1;
         line_cnt  = 0;
         pixel_cnt = 0;
         
         repeat (vsync_pulse) begin
            repeat (hsync_pulse) begin
               vsync = 1'b1;
               hsync = 1'b1;
               @(negedge refclk_i);
            end
            repeat (hback_porch+total_pix+hfront_porch) begin
               vsync = 1'b1;
               hsync = 1'b0;
               @(negedge refclk_i);
            end
         end

         repeat (vback_porch) begin
            repeat (hsync_pulse) begin
               vsync = 1'b0;
               hsync = 1'b1;
               @(negedge refclk_i);
            end
            repeat (hback_porch+total_pix+hfront_porch) begin
               vsync = 1'b0;
               hsync = 1'b0;
               @(negedge refclk_i);
            end
         end   

         repeat (total_line) begin
    
            line_cnt  = line_cnt + 1;
            pixel_cnt = 0;  

            repeat (hsync_pulse) begin
               vsync = 1'b0;
               hsync = 1'b1;
               @(negedge refclk_i);
            end     
        
            repeat (hback_porch) begin
               vsync = 1'b0;
               hsync = 1'b0;
               @(negedge refclk_i);
            end
     
            repeat (total_pix) begin
               de = 1'b1;
               red = $random;
               green = $random;
               blue = $random;
               pixel_cnt = pixel_cnt + 1;
               $display("%t : FRAME : %2d | LINE : %4d | PIXEL : %4d | RED = %h | GREEN = %h | BLUE = %h", $time, frame_cnt, line_cnt, pixel_cnt, red, green, blue);
               @(negedge refclk_i);
            end

            de = 1'b0;
            red = 0;
            green = 0;
            blue = 0;

            repeat (hfront_porch) begin
               vsync = 1'b0;
               hsync = 1'b0;
               @(negedge refclk_i);
            end
         end
     
         repeat (vfront_porch) begin   
            repeat (hsync_pulse) begin
               vsync = 1'b0;
               hsync = 1'b1;
               @(negedge refclk_i);
            end
            repeat (hback_porch+total_pix+hfront_porch) begin
               vsync = 1'b0;
               hsync = 1'b0;
               @(negedge refclk_i);
            end
         end    
      end   

      #100000;
      $display("%0t TEST END\n",$time);
      $finish;
   end


   PUR PUR_INST(resetn);

    SIP7_inst  I_rgb_2_dphy (
//------Common Interface Ports
        .pix_clk_i(refclk_w ),        // pixel or refclk clock
        .reset_n_i(resetn ),          // (active low) asynchronous reset
        .pd_dphy_i(0),                // DPHY PD signal

//------Debug Signals available if MISC_ON is defined
`ifdef MISC_ON
        .tinit_done_o(tinit_done),    // Tinit done
        .pll_lock_o  (pll_lock),      // PLL clock lock signal
`endif // MISC_ON

//------DSI Interface Ports
        .vsync_i     (vsync),         // vertical sync input for CMOS interface
        .hsync_i     (hsync),         // horizontal sync input for CMOS interface
        .de_i        (de),            // data enable input for CMOS interface
        .pixdata_d0_i(pixdata_d0_i),  // pixel data for CMOS interface
`ifdef MISC_ON
        .dcsrom_done_o(dcsrom_done),  // complete sending DCS ROM commands
`endif // MISC_ON

// DPHY output ports
`ifdef NUM_TX_LANE_1
        .d0_p_io(),       // DPHY output data 0
        .d0_n_io(),       // DPHY output data 0
`elsif NUM_TX_LANE_2
        .d0_p_io(),       //DPHY output data 0
        .d0_n_io(),       //DPHY output data 0
        .d1_p_o (),        //DPHY output data 1
        .d1_n_o (),        //DPHY output data 1
`elsif NUM_TX_LANE_4
        .d0_p_io(),       //DPHY output data 0
        .d0_n_io(),       //DPHY output data 0
        .d1_p_o (),        //DPHY output data 1
        .d1_n_o (),        //DPHY output data 1
        .d2_p_o (),        //DPHY output data 2
        .d2_n_o (),        //DPHY output data 2
        .d3_p_o (),        //DPHY output data 3
        .d3_n_o (),        //DPHY output data 3
`endif // NUM_TX_LANE
        .clk_p_o(),       // DPHY output clock
        .clk_n_o()        // DPHY output clock
     );


   initial begin
      $shm_open("./dump.shm");
      $shm_probe(top, ("AC"));
   end

   always #(refclk_period/2) refclk_i =~ refclk_i;

endmodule

`endif
