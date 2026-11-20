# Level 2: rotate right and left (Fig 11.68b)
import cocotb
from common import run


@cocotb.test()
async def test_rotate_right(dut):
    await run(dut, [dict(left=0)])


@cocotb.test()
async def test_rotate_left(dut):
    await run(dut, [dict(left=1)])
