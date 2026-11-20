# Level 3: rotates plus logical and arithmetic shifts (Fig 11.68c)
import cocotb
from common import run


@cocotb.test()
async def test_rotate_right(dut):
    await run(dut, [dict(left=0, shift=0)])


@cocotb.test()
async def test_rotate_left(dut):
    await run(dut, [dict(left=1, shift=0)])


@cocotb.test()
async def test_logical_right(dut):
    await run(dut, [dict(left=0, shift=1, arithmetic=0)])


@cocotb.test()
async def test_arithmetic_right(dut):
    await run(dut, [dict(left=0, shift=1, arithmetic=1)])


@cocotb.test()
async def test_shift_left(dut):
    await run(dut, [dict(left=1, shift=1, arithmetic=0),
                    dict(left=1, shift=1, arithmetic=1)])   # arith left == logical left
