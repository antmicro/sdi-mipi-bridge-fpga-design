TEMP=/tmp
DIAMOND_DIR=/usr/local/diamond/3.12/

verilog/720p:
	cd  antmicro-sdi-bridge-sdi-mipi-ip && make verilog/720p

verilog/1080p:
	cd  antmicro-sdi-bridge-sdi-mipi-ip && make verilog/1080p

clean:
	cd  antmicro-sdi-bridge-sdi-mipi-ip && make clean/verilog

bitgen: verilog/720p
	export TEMP=${TEMP}
	export LSC_INI_PATH=""
	export LSC_DIAMOND=true
	export TCL_LIBRARY=${DIAMOND_DIR}/tcltk/lib/tcl8.5
	export FOUNDRY=${DIAMOND_DIR}/ispFPGA
	export PATH=$FOUNDRY/bin/lin64:$PATH
	${DIAMOND_DIR}/bin/lin64/diamondc bitgen.tcl | tee mipi_tester.log

