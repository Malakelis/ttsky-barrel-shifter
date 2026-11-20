# Usage:
#   make LEVEL=1 N=4     -> n_ror_barrel.v + test_ror.py
#   make LEVEL=2 N=8     -> n_ror_l.v   + test_ror_l.py
#   make LEVEL=3 N=16    -> n_shifter.v + test_shifter.py
#   make regress       -> every level at N = 4, 8, 16

LEVEL ?= 1
N     ?= 4
export N

SIM ?= icarus
TOPLEVEL_LANG ?= verilog
SRC = $(PWD)/../../src

ifeq ($(LEVEL),1)
  VERILOG_SOURCES = $(SRC)/n_ror_barrel.v
  COCOTB_TOPLEVEL = n_ror_barrel
  COCOTB_TEST_MODULES = test_ror
else ifeq ($(LEVEL),2)
  VERILOG_SOURCES = $(SRC)/n_ror_l.v
  COCOTB_TOPLEVEL = n_ror_l
  COCOTB_TEST_MODULES = test_ror_l
else
  VERILOG_SOURCES = $(SRC)/n_shifter.v
  COCOTB_TOPLEVEL = n_shifter
  COCOTB_TEST_MODULES = test_shifter
endif

COMPILE_ARGS += -P$(COCOTB_TOPLEVEL).N=$(N)
SIM_BUILD = sim_build/L$(LEVEL)_N$(N)

include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: regress
regress:
	@for l in 1 2 3; do for n in 4 8 16; do \
	  $(MAKE) --no-print-directory sim LEVEL=$$l N=$$n || exit 1; \
	done; done
