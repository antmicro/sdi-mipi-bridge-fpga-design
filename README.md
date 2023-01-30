# SDI to MIPI CSI-2 Bridge FPGA design

Copyright 2023 [Antmicro](https://antmicro.com/)

## Introduction

This is a SDI to MIPI CSI-2 bridge design for Lattice Diamond tool.

The design uses video data acquired from the Semtech GS2971A deserializer
to generate correct MIPI timings. It converts hsync and vsync signals
to lv and fv that are passed down to CMOS2DPHY IP Core
for Lattice Crosslink devices.

## Contents

The project consist of:
* [SDI2MIPI](src/sdi2mipi.py) IP - block written in python with Migen to generate correct
timings for the MIPI transmitter from synchronization signals acquired from
SDI deserializer.
* [Lattice CMOS2DPHY IP Core](https://www.latticesemi.com/en/Products/DesignSoftwareAndIP/IntellectualProperty/IPCore/IPCores04/CMOStoMIPICSI2InterfaceBridge) - for converting and transmitting parallelized data in MIPI CSI-2 standard.

## Setup

The design in this repository is prepared for Lattice Diamond tool. It is
required to install it in order to generate the bitstream and program the device.
For instructions on installation and usage of Diamond, please refer to
[Lattice Diamond 3.12 Installation Notice for Linux](https://www.latticesemi.com/-/media/LatticeSemi/Documents/Diamond312/Diamond_Install_Linux.ashx).

Additionally, make sure that you installed sources of `CMOS to D-PHY 1.3` IP-Core
using Diamond Clarity Designer. For more information, check
[Accomplishing Tasks with Clarity Designer](https://www.latticesemi.com/-/media/LatticeSemi/Documents/UserManuals/1D/ClarityUserGuide32.ashx#page=11)
from Clarity Designer User Manual (p. 11).

Once you have Diamond prepared, install Python prerequisites:
```
pip3 install -r requirements.txt
```

## Build

After you've prepared your environment, you can build the project with the following command:
```
./run --video-format=<video-format> --lanes=<lanes>
```
where:

* `<video-format>` - is one of `720p60`, `1080p30`, `1080p60`
* `<lanes>` - is `2` or `4`

The output files will be generated in the `build/<video-format>-<lanes>` directory.

## Software

Detailed instruction about software support is available in [SDI MIPI Bridge repository](https://github.com/antmicro/sdi-mipi-bridge/blob/master/sw_setup_l4t.rst).
