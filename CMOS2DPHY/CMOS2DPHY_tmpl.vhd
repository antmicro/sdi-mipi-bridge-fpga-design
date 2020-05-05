--VHDL instantiation template

component CMOS2DPHY is
    port (csi2_inst_pixdata_d0_i: in std_logic_vector(23 downto 0);
        csi2_inst_clk_n_o: inout std_logic;
        csi2_inst_clk_p_o: inout std_logic;
        csi2_inst_d0_n_io: inout std_logic;
        csi2_inst_d0_p_io: inout std_logic;
        csi2_inst_d1_n_o: inout std_logic;
        csi2_inst_d1_p_o: inout std_logic;
        csi2_inst_dvalid_i: in std_logic;
        csi2_inst_fv_i: in std_logic;
        csi2_inst_lv_i: in std_logic;
        csi2_inst_pd_dphy_i: in std_logic;
        csi2_inst_pix_clk_i: in std_logic;
        csi2_inst_pll_lock_o: out std_logic;
        csi2_inst_reset_n_i: in std_logic;
        csi2_inst_tinit_done_o: out std_logic
    );
    
end component CMOS2DPHY; -- sbp_module=true 
_inst: CMOS2DPHY port map (csi2_inst_pixdata_d0_i => __,csi2_inst_clk_n_o => __,
            csi2_inst_clk_p_o => __,csi2_inst_d0_n_io => __,csi2_inst_d0_p_io => __,
            csi2_inst_d1_n_o => __,csi2_inst_d1_p_o => __,csi2_inst_dvalid_i => __,
            csi2_inst_fv_i => __,csi2_inst_lv_i => __,csi2_inst_pd_dphy_i => __,
            csi2_inst_pix_clk_i => __,csi2_inst_pll_lock_o => __,csi2_inst_reset_n_i => __,
            csi2_inst_tinit_done_o => __);
