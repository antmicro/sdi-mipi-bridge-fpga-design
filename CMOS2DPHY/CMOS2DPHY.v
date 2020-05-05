/* synthesis translate_off*/
`define SBP_SIMULATION
/* synthesis translate_on*/
`ifndef SBP_SIMULATION
`define SBP_SYNTHESIS
`endif

//
// Verific Verilog Description of module CMOS2DPHY
//
module CMOS2DPHY (csi2_inst_pixdata_d0_i, csi2_inst_clk_n_o, csi2_inst_clk_p_o, 
            csi2_inst_d0_n_io, csi2_inst_d0_p_io, csi2_inst_d1_n_o, csi2_inst_d1_p_o, 
            csi2_inst_dvalid_i, csi2_inst_fv_i, csi2_inst_lv_i, csi2_inst_pd_dphy_i, 
            csi2_inst_pix_clk_i, csi2_inst_pll_lock_o, csi2_inst_reset_n_i, 
            csi2_inst_tinit_done_o) /* synthesis sbp_module=true */ ;
    input [23:0]csi2_inst_pixdata_d0_i;
    inout csi2_inst_clk_n_o;
    inout csi2_inst_clk_p_o;
    inout csi2_inst_d0_n_io;
    inout csi2_inst_d0_p_io;
    inout csi2_inst_d1_n_o;
    inout csi2_inst_d1_p_o;
    input csi2_inst_dvalid_i;
    input csi2_inst_fv_i;
    input csi2_inst_lv_i;
    input csi2_inst_pd_dphy_i;
    input csi2_inst_pix_clk_i;
    output csi2_inst_pll_lock_o;
    input csi2_inst_reset_n_i;
    output csi2_inst_tinit_done_o;
    
    
    csi2_inst csi2_inst_inst (.pixdata_d0_i({csi2_inst_pixdata_d0_i}), .clk_n_o(csi2_inst_clk_n_o), 
            .clk_p_o(csi2_inst_clk_p_o), .d0_n_io(csi2_inst_d0_n_io), .d0_p_io(csi2_inst_d0_p_io), 
            .d1_n_o(csi2_inst_d1_n_o), .d1_p_o(csi2_inst_d1_p_o), .dvalid_i(csi2_inst_dvalid_i), 
            .fv_i(csi2_inst_fv_i), .lv_i(csi2_inst_lv_i), .pd_dphy_i(csi2_inst_pd_dphy_i), 
            .pix_clk_i(csi2_inst_pix_clk_i), .pll_lock_o(csi2_inst_pll_lock_o), 
            .reset_n_i(csi2_inst_reset_n_i), .tinit_done_o(csi2_inst_tinit_done_o));
    
endmodule

