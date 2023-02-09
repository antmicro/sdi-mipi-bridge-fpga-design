# SDI to MIPI CSI-2 Bridge FPGA design

Copyright 2021-2023 [Antmicro](https://antmicro.com/)

## Introduction

This is the FPGA design for the SDI to MIPI CSI-2 bridge.
The design targets the Lattice Diamond toolchain and uses video data acquired
from the Semtech GS2971A deserializer to generate correct MIPI timings.
It converts `hsync` and `vsync` signals to `lv` and `fv` that are passed down
to the CMOS2DPHY IP Core in the on-board Lattice Crosslink.

## Contents

The project consist of:

* [SDI2MIPI](src/sdi2mipi.py) IP - block written in Python with Migen to generate correct
timings for the MIPI transmitter from synchronization signals acquired from the
SDI deserializer.
* [Lattice CMOS2DPHY IP Core](https://www.latticesemi.com/en/Products/DesignSoftwareAndIP/IntellectualProperty/IPCore/IPCores04/CMOStoMIPICSI2InterfaceBridge) - for converting and transmitting parallelized data in the MIPI CSI-2 standard.

## Setup

The design in this repository is prepared for the Lattice Diamond tool, which is needed for generating the bitstream and programming the device.
For instructions on installing and using Diamond, please refer to the [Lattice Diamond 3.12 Installation Notice for Linux](https://www.latticesemi.com/-/media/LatticeSemi/Documents/Diamond312/Diamond_Install_Linux.ashx).

Additionally, make sure that you installed the sources of the `CMOS to D-PHY 1.3` IP-Core using the Diamond Clarity Designer.
For more information, check [Accomplishing Tasks with Clarity Designer](https://www.latticesemi.com/-/media/LatticeSemi/Documents/UserManuals/1D/ClarityUserGuide32.ashx#page=11)
from Clarity Designer User Manual (p. 11).

Once you have Diamond set up, install Python prerequisites:

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

Detailed instructions about software support is available in the [SDI MIPI Bridge repository](https://github.com/antmicro/sdi-mipi-bridge/blob/master/sw_setup_l4t.rst).
