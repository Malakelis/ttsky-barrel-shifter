# Level 1: rotate right only (Fig 11.68a)
import cocotb
from common import run


@cocotb.test()
async def test_rotate_right(dut):
    await run(dut, [dict()])
