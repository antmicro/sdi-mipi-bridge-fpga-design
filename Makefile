# Copyright 2023 Antmicro <www.antmicro.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


define GENERATE_PROJECT =
python3 build.py --video-format=$(1) --lanes=$(2)
endef

.PHONY: format
format: ## Format sources
	python3 -m black .

.PHONY: format-diff
format-diff: ## Print formatter diff for each source file
	python3 -m black --diff .

.PHONY: 720p_hd-2lanes
720p_hd-2lanes: build/720p_hd-2lanes ## Generate bitstream for 720p25, 720p30, 720p50 and 720p60 video format, 2 lanes

build/720p_hd-2lanes: build.py
build/720p_hd-2lanes: lattice/CMOS2DPHY/CMOS2DPHY.v
build/720p_hd-2lanes: lattice/CMOS2DPHY/generate_core.tcl
build/720p_hd-2lanes: lattice/CMOS2DPHY/720p_hd-2lanes/CMOS2DPHY.sbx
build/720p_hd-2lanes: lattice/CMOS2DPHY/720p_hd-2lanes/csi2_inst.lpc
build/720p_hd-2lanes: | $(BUILD_DIR)
	$(call GENERATE_PROJECT,720p_hd,2)

.PHONY: 720p_hd-4lanes
720p_hd-4lanes: build/720p_hd-4lanes ## Generate bitstream for 720p25, 720p30, 720p50 and 720p60 video format, 4 lanes

build/720p_hd-4lanes: build.py
build/720p_hd-4lanes: lattice/CMOS2DPHY/CMOS2DPHY.v
build/720p_hd-4lanes: lattice/CMOS2DPHY/generate_core.tcl
build/720p_hd-4lanes: lattice/CMOS2DPHY/720p_hd-4lanes/CMOS2DPHY.sbx
build/720p_hd-4lanes: lattice/CMOS2DPHY/720p_hd-4lanes/csi2_inst.lpc
build/720p_hd-4lanes: | $(BUILD_DIR)
	$(call GENERATE_PROJECT,720p_hd,4)

.PHONY: 1080p_hd-2lanes
1080p_hd-2lanes: build/1080p_hd-2lanes ## Generate bitstream for 1080p25 and 1080p30 video format, 2 lanes

build/1080p_hd-2lanes: build.py
build/1080p_hd-2lanes: lattice/CMOS2DPHY/CMOS2DPHY.v
build/1080p_hd-2lanes: lattice/CMOS2DPHY/generate_core.tcl
build/1080p_hd-2lanes: lattice/CMOS2DPHY/1080p_hd-2lanes/CMOS2DPHY.sbx
build/1080p_hd-2lanes: lattice/CMOS2DPHY/1080p_hd-2lanes/csi2_inst.lpc
build/1080p_hd-2lanes: | $(BUILD_DIR)
	$(call GENERATE_PROJECT,1080p_hd,2)

.PHONY: 1080p_hd-4lanes
1080p_hd-4lanes: build/1080p_hd-4lanes ## Generate bitstream for 1080p25 and 1080p30 video format, 4 lanes

build/1080p_hd-4lanes: build.py
build/1080p_hd-4lanes: lattice/CMOS2DPHY/CMOS2DPHY.v
build/1080p_hd-4lanes: lattice/CMOS2DPHY/generate_core.tcl
build/1080p_hd-4lanes: lattice/CMOS2DPHY/1080p_hd-4lanes/CMOS2DPHY.sbx
build/1080p_hd-4lanes: lattice/CMOS2DPHY/1080p_hd-4lanes/csi2_inst.lpc
build/1080p_hd-4lanes: | $(BUILD_DIR)
	$(call GENERATE_PROJECT,1080p_hd,4)

.PHONY: 1080p_3g-2lanes
1080p_3g-2lanes: build/1080p_3g-2lanes ## Generate bitstream for 1080p50 and 1080p60 video format, 2 lanes

build/1080p_3g-2lanes: build.py
build/1080p_3g-2lanes: lattice/CMOS2DPHY/CMOS2DPHY.v
build/1080p_3g-2lanes: lattice/CMOS2DPHY/generate_core.tcl
build/1080p_3g-2lanes: lattice/CMOS2DPHY/1080p_3g-2lanes/CMOS2DPHY.sbx
build/1080p_3g-2lanes: lattice/CMOS2DPHY/1080p_3g-2lanes/csi2_inst.lpc
build/1080p_3g-2lanes: | $(BUILD_DIR)
	$(call GENERATE_PROJECT,1080p_3g,2)

.PHONY: 1080p_3g-4lanes
1080p_3g-4lanes: build/1080p_3g-4lanes ## Generate bitstream for 1080p50 and 1080p60 video format, 4 lanes

build/1080p_3g-4lanes: build.py
build/1080p_3g-4lanes: lattice/CMOS2DPHY/CMOS2DPHY.v
build/1080p_3g-4lanes: lattice/CMOS2DPHY/generate_core.tcl
build/1080p_3g-4lanes: lattice/CMOS2DPHY/1080p_3g-4lanes/CMOS2DPHY.sbx
build/1080p_3g-4lanes: lattice/CMOS2DPHY/1080p_3g-4lanes/csi2_inst.lpc
build/1080p_3g-4lanes: | $(BUILD_DIR)
	$(call GENERATE_PROJECT,1080p_3g,4)

$(BUILD_DIR):
	mkdir -p $@

HELP_COLUMN_SPAN = 30
HELP_FORMAT_STRING = "\033[36m%-$(HELP_COLUMN_SPAN)s\033[0m %s\n"
.PHONY: help
help: ## Show this help message
	@echo Here is the list of available targets:
	@echo ""
	@grep -hE '^[^#[:blank:]]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf $(HELP_FORMAT_STRING), $$1, $$2}'
	@echo ""
