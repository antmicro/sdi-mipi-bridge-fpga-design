PYTHON_GEN = aligner.py
IVER_O = aligner
V_SRC = align_tb.v aligner.v

all:
	@true

align:
	python3 $(PYTHON_GEN)

sim: align
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

ci_sim:
	iverilog -o $(IVER_O) $(V_SRC)
	vvp $(IVER_O)

clean/sim:
	rm -f $(IVER_O)

clean/align:
	rm -f aligner.v

clean/vcd:
	rm -f *.vcd

clean: clean/sim clean/vcd
	@true

clean/all: clean clean/align
	@true
