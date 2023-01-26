//===========================================================================
// Verilog file generated by Clarity Designer    08/05/2020    12:44:46  
// Filename  : csi2_inst_DCS_hs_bb.v                                                
// IP package: CMOS to D-PHY 1.3                           
// Copyright(c) 2016 Lattice Semiconductor Corporation. All rights reserved. 
//===========================================================================
`timescale 1ns/1ps

module csi2_inst_DCS_hs 
(
////added ports for handshaking with LP HS controller
    input                          d_hs_rdy_i,
    output                         d_hs_en_o,

    input                          reset_n,
    input                          clk,
    input      [16:0]       q_hs_data_d, //{trail ind, data}
    output     [10-1:0]  hs_cmd_cnt,
    output                         hs_en  ,
    output     [16-1:0]     q_hs_data /*synthesis syn_ramstyle = "EBR"*/,
    output                         hs_dcs_done
);

endmodule                         
