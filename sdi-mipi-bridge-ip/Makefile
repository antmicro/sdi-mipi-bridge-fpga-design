PYTHON_GEN = timing_gen_tb.py
IVER_O = sdi2mipi
FRAMES = 2
V_SRC = $(shell find . -print | grep '\.v$$' | grep -v '_tb\.v$$') sdi2mipi_tb.v

verilog/720p:
	cd timing && make tim/720p
	cd detector && make detect
	cd aligner && make align

verilog/1080p:
	cd timing && make tim/1080p
	cd detector && make detect
	cd aligner && make align

clean/verilog:
	cd timing && make clean/tim
	cd detector && make clean/detect
	cd aligner && make clean/align

sim: verilog/720p
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

ci_sim:
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

clean/sim:
	rm -f $(IVER_O)

clean/vcd:
	rm -f *.vcd

clean: clean/vcd clean/sim
	@true

clean/all: clean clean/verilog
	@true
