# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def tt_init_state(dut):
	dut._log.info("Start Testcase: Check initial states and outputs")
	
	dut.ena.value = 1
	dut.s_set_coeffs.value = 0
	dut.s_axis_fir_tvalid.value = 1
	dut.s_axis_fir_tdata.value = BinaryValue('00000000')
	
	
	#start clock
	cocotb.start_soon(Clock(dut.clk, 16, units="ns").start())
	
	
	print_func(dut, 'test')

def print_func(dut, text):
	dut._log.info(text)
	
async def not_called(dut):
	dut._log.info('this shouldnt be called')

@cocotb.test()
async def test_adder(dut):
  dut._log.info("Start")
  
  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  # Set the input values, wait one clock cycle, and check the output
  dut._log.info("Test")
  dut.ui_in.value = 20
  dut.uio_in.value = 30

  await ClockCycles(dut.clk, 1)
  
  dut._log.info("Start FIR Testing")
  
