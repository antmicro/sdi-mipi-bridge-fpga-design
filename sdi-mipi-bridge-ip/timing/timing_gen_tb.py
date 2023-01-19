from migen import *
from migen.fhdl.verilog import convert
from timing_gen import TimingGenerator
from datetime import datetime
import sys
import argparse

supported_res = ["1080p60", "720p60"]

###

H_ACTIVE      = 1280
H_BACK_PORCH  = 220
H_SYNC        = 40
H_FRONT_PORCH = 110
H_TOTAL       = H_ACTIVE + H_BACK_PORCH + H_SYNC + H_FRONT_PORCH
V_ACTIVE      = 720
V_BACK_PORCH  = 20
V_SYNC        = 5
V_FRONT_PORCH = 5
V_TOTAL       = V_ACTIVE + V_BACK_PORCH + V_SYNC + V_FRONT_PORCH

def main():
    parser = argparse.ArgumentParser(description="Pick timings, generate verilog and simulate the generator")

    parser.add_argument("-g", "--generate", nargs="?", default="timing_gen", help="set the name of verilog module and output file, defaults to 'timing_gen'")
    parser.add_argument("-s", "--simulate", action="store_true", help="simulate the generator")
    parser.add_argument("-f", "--frames", type=int, nargs="?", default="1", help="specify how many frames will be simulated, defaults to 1")
    parser.add_argument("timings", metavar="T", default="default", nargs="?", help="timing specifier string, defaults to global variables at the beginning of the script")

    args = parser.parse_args()
    arg = vars(args)

    timings = {}
    if (arg["timings"] != "default"):
        if (arg["timings"] in supported_res):
            timings = form_params(arg["timings"])
        else:
            raise NameError("Unsupported timings!")
    else:
        timings = form_params(arg["timings"])
    if (arg["generate"] is None):
        raise NameError("Module name not specified!")
    else:
        gen = TimingGenerator(timings)
        convert(gen, gen.ios, name=arg["generate"]).write(arg["generate"] + ".v")
        print("Verilog output saved to " + arg["generate"] + ".v")

    if (arg["simulate"]):
        gen = TimingGenerator(timings)
        if (arg["frames"] is None):
            raise NameError("frame number not specified!")
        else:
            run_simulation(gen, test_bench(gen, timings, arg["frames"]),
                           clocks={"pix": 14},
                           vcd_name="sim_" + arg["timings"] + ".vcd")

def test_bench(dut, timings, frames):
    H_ACTIVE      = timings["H_ACTIVE"]
    H_BACK_PORCH  = timings["H_BACK_PORCH"]
    H_SYNC        = timings["H_SYNC"]
    H_FRONT_PORCH = timings["H_FRONT_PORCH"]
    H_TOTAL       = timings["H_TOTAL"]
    V_ACTIVE      = timings["V_ACTIVE"]
    V_BACK_PORCH  = timings["V_BACK_PORCH"]
    V_SYNC        = timings["V_SYNC"]
    V_FRONT_PORCH = timings["V_FRONT_PORCH"]
    V_TOTAL       = timings["V_TOTAL"]

    prntt("Simulation started")
    prntt("Frames to simulate: " + str(frames))
    prntt("Timings:")
    prntt("H_ACTIVE     :   " + str(H_ACTIVE))
    prntt("H_BACK_PORCH :   " + str(H_BACK_PORCH))
    prntt("H_SYNC       :   " + str(H_SYNC))
    prntt("H_FRONT_PORCH:   " + str(H_FRONT_PORCH))
    prntt("H_TOTAL      :   " + str(H_TOTAL))
    prntt("V_ACTIVE     :   " + str(V_ACTIVE))
    prntt("V_BACK_PORCH :   " + str(V_BACK_PORCH))
    prntt("V_SYNC       :   " + str(V_SYNC))
    prntt("V_FRONT_PORCH:   " + str(V_FRONT_PORCH))
    prntt("V_TOTAL      :   " + str(V_TOTAL))

    (yield dut.n_rst.eq(1))
    for i in range(0, 10):
        yield
        yield
    (yield dut.n_rst.eq(0))
    for i in range(0, 4):
        yield
        yield
    (yield dut.n_rst.eq(1))
    for i in range(0, 10):
        yield
        yield
    for j in range(0, frames):
        l = 1
        (yield dut.vsync_i.eq(1))
        yield
        for k in range(0, V_SYNC):
            (yield dut.hsync_i.eq(1))
            yield
            for i in range(0, H_SYNC):
                yield
                yield
            (yield dut.hsync_i.eq(0))
            yield
            for i in range(0, H_BACK_PORCH + H_ACTIVE + H_FRONT_PORCH):
                yield
                yield
            prntt("Frame " + str(j + 1) + ", Line " + str(l) + " done")
            l += 1
        (yield dut.vsync_i.eq(0))
        yield
        for k in range(0, V_TOTAL - V_SYNC):
            (yield dut.hsync_i.eq(1))
            yield
            for i in range(0, H_SYNC):
                yield
                yield
            (yield dut.hsync_i.eq(0))
            yield
            for i in range(0, H_BACK_PORCH + H_ACTIVE + H_FRONT_PORCH):
                yield
                yield
            prntt("Frame " + str(j + 1) + ", Line " + str(l) + " done")
            l += 1
        prntt("Frame " + str(j + 1) + " done")

def form_params(res):
    timings = {}

    if (res == "1080p60"):
        timings["H_ACTIVE"]      = 1920
        timings["H_BACK_PORCH"]  = 148
        timings["H_SYNC"]        = 44
        timings["H_FRONT_PORCH"] = 88
        timings["H_TOTAL"]       = 0
        timings["V_ACTIVE"]      = 1080
        timings["V_BACK_PORCH"]  = 36
        timings["V_SYNC"]        = 5
        timings["V_FRONT_PORCH"] = 4
        timings["V_TOTAL"]       = 0
    elif (res == "720p60"):
        timings["H_ACTIVE"]      = 1280
        timings["H_BACK_PORCH"]  = 220
        timings["H_SYNC"]        = 40
        timings["H_FRONT_PORCH"] = 110
        timings["H_TOTAL"]       = 0
        timings["V_ACTIVE"]      = 720
        timings["V_BACK_PORCH"]  = 20
        timings["V_SYNC"]        = 5
        timings["V_FRONT_PORCH"] = 5
        timings["V_TOTAL"]       = 0
    else:
        timings["H_ACTIVE"]      = H_ACTIVE
        timings["H_BACK_PORCH"]  = H_BACK_PORCH
        timings["H_SYNC"]        = H_SYNC
        timings["H_FRONT_PORCH"] = H_FRONT_PORCH
        timings["H_TOTAL"]       = H_TOTAL
        timings["V_ACTIVE"]      = V_ACTIVE
        timings["V_BACK_PORCH"]  = V_BACK_PORCH
        timings["V_SYNC"]        = V_SYNC
        timings["V_FRONT_PORCH"] = V_FRONT_PORCH
        timings["V_TOTAL"]       = V_TOTAL

    timings["H_TOTAL"] = timings["H_ACTIVE"] + timings["H_SYNC"] + \
                         timings["H_BACK_PORCH"] + timings["H_FRONT_PORCH"]
    timings["V_TOTAL"] = timings["V_ACTIVE"] + timings["V_SYNC"] + \
                         timings["V_BACK_PORCH"] + timings["V_FRONT_PORCH"]

    print("Running with " + res + " timings")
    return timings

def prntt(msg):
    time = datetime.now().time()
    print(str(time) + ": " + msg)

if __name__ == "__main__":
    main()

