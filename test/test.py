# SPDX-FileCopyrightText: © 2026 Alan Aquino
# SPDX-License-Identifier: Apache-2.0
#
# Top-level (tt_um_barrel_shifter) test: exhaustive 8-bit check of every
# operation against the golden model. Also runs on the gate-level netlist.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

from model import model

N = 8

# (name, left, shift, arithmetic)
MODES = [
    ("rotate right",     0, 0, 0),
    ("rotate left",      1, 0, 0),
    ("logical right",    0, 1, 0),
    ("arithmetic right", 0, 1, 1),
    ("shift left",       1, 1, 0),
    ("shift left (arith bit set)", 1, 1, 1),
]


async def reset(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1


async def run_mode(dut, name, left, shift, arith):
    errors = 0
    for k in range(N):
        for a in range(1 << N):
            dut.ui_in.value = a
            dut.uio_in.value = k | (left << 3) | (shift << 4) | (arith << 5)
            await Timer(1, unit="ns")
            got = int(dut.uo_out.value)
            exp = model(a, k, N, left, shift, arith)
            if got != exp:
                errors += 1
                dut._log.error(f"{name}: a={a:08b} k={k} got {got:08b} expected {exp:08b}")
                assert errors < 10, "Stopping after 10 errors"
    assert errors == 0


@cocotb.test()
async def test_all_modes(dut):
    dut._log.info("Start")
    await reset(dut)
    for name, left, shift, arith in MODES:
        dut._log.info(f"Testing {name}")
        await run_mode(dut, name, left, shift, arith)


@cocotb.test()
async def test_bidir_pins_are_inputs(dut):
    await reset(dut)
    assert int(dut.uio_oe.value) == 0
    assert int(dut.uio_out.value) == 0
