# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.triggers import Timer


async def tick(dut):
    await Timer(5, unit="us")
    dut.clk.value = 1
    await Timer(5, unit="us")
    dut.clk.value = 0


@cocotb.test()
async def traffic_light_sequence(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.clk.value = 0
    dut.rst_n.value = 0

    await tick(dut)
    assert int(dut.uo_out.value) == 0b001, "Reset should select red"
    await tick(dut)
    assert int(dut.uo_out.value) == 0b001, "Holding reset should keep red on"

    dut.rst_n.value = 1
    # Bits 2, 1 and 0 are green, amber and red, respectively.
    for expected, name in [
        (0b011, "red and amber"),
        (0b100, "green"),
        (0b010, "amber"),
        (0b001, "red"),
    ]:
        await tick(dut)
        assert int(dut.uo_out.value) == expected, f"Expected {name}"

    # Reset again from green to check that the circuit can restart mid-cycle.
    await tick(dut)
    await tick(dut)
    assert int(dut.uo_out.value) == 0b100
    dut.rst_n.value = 0
    await tick(dut)
    assert int(dut.uo_out.value) == 0b001
    assert int(dut.uio_out.value) == 0
    assert int(dut.uio_oe.value) == 0
