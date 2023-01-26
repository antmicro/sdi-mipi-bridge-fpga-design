# SDI to MIPI CSI-2 Bridge FPGA design

## Introduction

This is a SDI to MIPI CSI-2 bridge design for Lattice Diamond tool. It is
prepared to run with SDI Bridge, on Lattice Crosslink FPGA.
Design is available in 3 versions - each on different branch, supporting:

| Resolution  | Branch  |
|-------------|---------|
| 1080p 60fps | 1080p60 |
| 1080p 30fps | 1080p30 |
| 720p 60fps  | master  |

## Contents

The project consist of:
* sdi-mipi IP - block written in python with Migen to generate correct
timings for the MIPI transmitter from synchronization signals acquired from
SDI deserializer.
* [Lattice CMOS2DPHY IP Core](https://www.latticesemi.com/en/Products/DesignSoftwareAndIP/IntellectualProperty/IPCore/IPCores04/CMOStoMIPICSI2InterfaceBridge) - for converting and transmitting parallelized data in MIPI CSI-2 standard.

## Setup

```bash
git clone <sdi-bridge-mipi-tester-repo>
cd antmicro-sdi-bridge-mipi-tester
git submodule update --init
```

The design is prepared for Lattice Diamond tool. It is required to install it
in order to generate the bitstream and program the device. For instructions on
installation and usage of Diamond please refer to `Diamond installation` and
`Diamond - getting started` sections of SDI to MIPI CSI-2
bridge documentation.

In order to use this design, verilog sources for timing generator blocks must
be generated. For prerequisites please refer to timing generator
instructions in README.
After installing Migen, verilog files can be generated with running in root directory

```bash
make verilog/720p
```
or
```bash
make verilog/1080p
```

---
**WARNING**

It is crucial to keep correct submodule version. Recomended way is to run:
```bash
git submodule update --init
```
for checking out submodule to commit that is binded with current design revision.

Then new verilog files must be generated on each submodule modification with:
```bash
make verilog/720p
```
or
```bash
make verilog/1080p
```

---

After generating verilog files bitstream can be generated in two ways:
* using Lattice Diamond GUI tool
* running `make bitgen`, **important:** make sure that `Makefile` has correct paths
  for Lattice Diamond tool in Your configuration

There is also a possibility of generating verilog files and bitstream in one
command: `make bitgen/res`, where `res` is desired resolution (pick from 720p or 1080p)

## HW test procedure

* Checkout on tested branch
* run `git submodule update --init`
* run `make verilog/res`, where `res` is tested resolution (pick from 720p or 1080p).
  Alternatively, download artifacts from first stage of submodule CI on given
  commit and put them in their directories according to their placement in
  diamond project
* generate bitstream
* program device

---
**NOTE**

Running 1080p 60fps design requires using CrossLink DDR (Double Data Rate)
capabilities. To run 1080p60 design, a proper deserializer configuration is needed.

Deserializer must be working in `SMPTE` mode (`!SMPTE_BYPASS` set to `HIGH`) and
configuration bit `LEVEL_B2A_CONV_DISABLE_MASK` must be tied to `LOW` in order
to enable video stream format conversion from `Level B` to `Level A`.

---
