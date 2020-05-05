//===========================================================================
// Filename: cmos_model.v
// Copyright(c) 2016 Lattice Semiconductor Corporation. All rights reserved. 
//===========================================================================
module cmos_model#(
   parameter num_frames           = 2,
   parameter num_lines            = 2,
   parameter num_pixels           = 200,
   parameter dwidth               = 8,

// timing related parameters
   parameter cmos_active_lines          = 3,
   parameter cmos_active_pixels         = 100,
   parameter cmos_fv_h_to_lv_h          = 10,
   parameter cmos_lv_l_to_lv_h          = 10,
   parameter cmos_lv_l_to_fv_l          = 10,
   parameter cmos_fv_l_to_fv_h          = 10,

   parameter cmos_bus_width             = 8,
   parameter long_even_line_en          = 0
)(
   input refclk_i,
   input resetn,
   input data_start,

   output [dwidth - 1 : 0]        cmos_data,
   output                         cmos_fv,
   output                         cmos_lv
);

reg [dwidth - 1 : 0] cmos_data_r;
reg                  cmos_fv_r;
reg                  cmos_lv_r;

assign cmos_data = cmos_data_r;
assign cmos_fv   = cmos_fv_r;
assign cmos_lv   = cmos_lv_r;

reg cmos_active;

integer i,j, pix_cnt;

initial begin
   cmos_data_r = 0;
   cmos_fv_r   = 0;
   cmos_lv_r   = 0;
   cmos_active = 0;

   @(posedge resetn);

   @(posedge cmos_active);
   $display("%t CMOS_MODEL: Model Activated", $time);

   repeat (num_frames) begin

       // fv_l to fv_h delay
       $display("%t CMOS_MODEL: Inserting fv_l to fv_h delay = %0d", $time, cmos_fv_l_to_fv_h);
       repeat (cmos_fv_l_to_fv_h) begin
          @(negedge refclk_i);
       end
       cmos_fv_r = 1;
    
       // fv_h to lv_h delay
       $display("%t CMOS_MODEL: Inserting fv_h to lv_h delay = %0d", $time, cmos_fv_h_to_lv_h);
       repeat (cmos_fv_h_to_lv_h) begin
          @(negedge refclk_i); 
       end
    
       drive_data;
    
       // lv_l to fv_l
       repeat (cmos_lv_l_to_fv_l) begin
          @(negedge refclk_i);
       end
       cmos_fv_r = 0;

   end

   repeat (1000) begin
      @(negedge refclk_i);
   end

   cmos_active = 0;
      
end


task drive_data;
begin
   for (j = 0; j < num_lines ; j = j + 1) begin
      if (long_even_line_en == 1) begin
         if (j[0:0] == 0) begin 
            pix_cnt = num_pixels; 
         end else
         begin
            pix_cnt = num_pixels *2;
         end
      end else
      begin
         pix_cnt = num_pixels;
      end

      for (i = 0 ; i < pix_cnt ; i = i + 1) begin
          cmos_lv_r   = 1;
          cmos_data_r = $urandom;
          $display("%t Driving Data : Line = %0d : Pixel[%0d] = %0x" , $time, j, i, cmos_data_r);
          @(negedge refclk_i);
      end
      cmos_lv_r   = 0;
      cmos_data_r = 0;
   
      if (j < num_lines - 1) begin
         $display("%t CMOS_MODEL: Inserting lv_l to lv_h delay = %0d", $time, cmos_lv_l_to_lv_h);
         repeat (cmos_lv_l_to_lv_h) begin
             @(negedge refclk_i);
         end
      end else
      begin
         $display("%t Last line transmitted", $time);
      end
   end
end
endtask

endmodule
