PYTHON_GEN = timing_gen_tb.py
IVER_O = timing
FRAMES = 2
V_SRC = timing_tb.v timing_gen.v

all:
	@true

tim/720p:
	python3 $(PYTHON_GEN) 720p60

tim/1080p:
	python3 $(PYTHON_GEN) 1080p60

tim:
	python3 $(PYTHON_GEN)

sim/720p: tim/720p
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

sim/1080p: tim/1080p
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

ci_sim/720p:
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

ci_sim/1080p:
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

clean/sim:
	rm -f $(IVER_O)

clean/tim:
	rm -f timing_gen.v

clean/vcd:
	rm -f timing.vcd

clean: clean/vcd clean/sim
	@true

clean/all: clean clean/tim
	@true
