PYTHON_GEN = detector.py
IVER_O = detector
V_SRC = detector_tb.v detector.v

all:
	@true

detect:
	python3 $(PYTHON_GEN)

sim: detect
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

ci_sim:
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

clean/sim:
	rm -f $(IVER_O)

clean/detect:
	rm -f detector.v

clean/vcd:
	rm -f *.vcd

clean: clean/sim clean/vcd
	@true

clean/all: clean clean/detect
	@true
