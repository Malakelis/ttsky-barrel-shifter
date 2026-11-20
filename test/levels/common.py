# Shared helpers for all three tests.
import os
import sys
from cocotb.triggers import Timer

# model.py lives one directory up (shared with the top-level test)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from model import model, vectors  # noqa: E402

N = int(os.environ.get("N", "4"))


async def check(dut, a, k, left=0, shift=0, arithmetic=0):
    """Drive one vector, wait for the logic to settle, compare to the model."""
    dut.data_in.value = a
    dut.k.value = k
    if hasattr(dut, "left"):
        dut.left.value = left
    if hasattr(dut, "shift"):
        dut.shift.value = shift
    if hasattr(dut, "arithmetic"):
        dut.arithmetic.value = arithmetic
    await Timer(1, unit="ns")

    got = int(dut.data_out.value)
    exp = model(a, k, N, left, shift, arithmetic)
    if got != exp:
        dut._log.error(f"a={a:0{N}b} k={k} left={left} shift={shift} arith={arithmetic}: "
                       f"got {got:0{N}b}, expected {exp:0{N}b}")
    return got == exp


async def run(dut, modes):
    """Run every (a, k) vector for each mode; fail if any mismatch."""
    errors = total = 0
    for mode in modes:
        for a, k in vectors(N):
            total += 1
            errors += not await check(dut, a, k, **mode)
            if errors >= 10:
                assert False, "Stopping after 10 errors"
    dut._log.info(f"N={N}: {total} vectors, {errors} errors")
    assert errors == 0
