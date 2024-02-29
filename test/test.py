# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, FallingEdge, ClockCycles, RisingEdge, Join, First
from cocotb.binary import BinaryValue

async def reset_dut(reset_n, duration_ns):
	reset_n.value = 0
	await Timer(duration_ns, units = "ns")
	reset_n.value = 1
	reset_n._log.info("dut reset completed")

#@cocotb.test()
async def tt_init_state(dut):
	dut._log.info("Start Testcase: Check initial states and outputs")
	
	dut.ena.value = 1
	dut.s_set_coeffs.value = 0
	dut.s_axis_fir_tvalid.value = 1
	dut.s_axis_fir_tdata.value = BinaryValue('00000001')
	
	
	#start clock
	cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())
	
	#reset dut
	await reset_dut(dut.rst_n, 20)
	
	await RisingEdge(dut.clk)
	
	dut.s_set_coeffs.value = 0
	dut.s_axis_fir_tvalid.value = 1
	dut.s_axis_fir_tdata.value = BinaryValue('00000001')
	
	
	await ClockCycles(dut.clk, 100)
	
	dut.s_axis_fir_tdata.value = BinaryValue('00000001')
	
	await ClockCycles(dut.clk, 10)
	
	dut._log.info(f'output val: {dut.m_axis_fir_tdata.value}')

	for i in range(8):
		dut._log.info(f'#{i:>03} -> {dut.m_axis_fir_tdata.value.binstr}')
	
	print_func(dut, 'test')

def print_func(dut, text):
	dut._log.info(text)
	
async def not_called(dut):
	dut._log.info('this shouldnt be called')

@cocotb.test()
async def test_impulse_response(dut):
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
  #dut.ui_in.value = 1
  #dut.ui_in.value = 1
  dut.s_axis_fir_tdata.value = 1
  dut.s_axis_fir_tvalid.value = 1
  dut.s_set_coeffs.value = 0
  #dut.uio_in.value = 30
  
  await ClockCycles(dut.clk, 10)
  
  dut.s_axis_fir_tdata.value = 0
  
  #testing if impulse response is correct - expected values - FIR Taps
  dut._log.info('Testing impulse response:')
  dut._log.info(f'expected output value: 00000000000 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000000'), 'impulse response wrong'
  await ClockCycles(dut.clk, 2)
  
  dut._log.info(f'expected output value: 11111111101 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('11111111101'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000010 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000010'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000011 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000011'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000011 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000011'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000010 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000010'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 11111111101 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('11111111101'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000000 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000000'), 'impulse response wrong'
  dut._log.info(f'impulse response correct!')
  
@cocotb.test()
async def test_fir_tap_configuration(dut):

  dut._log.info("Start")
  
  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 1, units="us") #10
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  #config new FIR Filter taps 
  dut._log.info('Configuring new FIR Filter taps...')
  dut.s_set_coeffs.value = 1
  await ClockCycles(dut.clk, 6) #5
  dut.s_axis_fir_tdata.value = 1
  await ClockCycles(dut.clk, 1)
  dut.s_axis_fir_tdata.value = 2
  await ClockCycles(dut.clk, 1)
  dut.s_axis_fir_tdata.value = 3
  dut.s_set_coeffs.value = 0
  await ClockCycles(dut.clk, 1)
  dut.s_axis_fir_tdata.value = 0
  dut._log.info('FIR Filter taps configured')
  
  
  await ClockCycles(dut.clk, 10)

  dut.s_axis_fir_tdata.value = 1
  dut.s_axis_fir_tvalid.value = 1
  #dut.uio_in.value = 30
  
  await ClockCycles(dut.clk, 6)
  
  dut.s_axis_fir_tdata.value = 0
  
  
  #testing if impulse response is correct - expected values - FIR Taps
  dut._log.info('Testing new configured impulse response:')
  await ClockCycles(dut.clk, 2)
  
  dut._log.info(f'expected output value: 00000000000 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000000'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000011 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000011'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000010 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000010'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000001 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000001'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000001 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000001'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000010 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000010'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000011 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000011'), 'impulse response wrong'
  await ClockCycles(dut.clk, 6)
  
  dut._log.info(f'expected output value: 00000000000 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000000000'), 'impulse response wrong'
  
  dut._log.info(f'impulse response correct!')
  
  await ClockCycles(dut.clk, 10) #100
  
  
  dut._log.info("Testing Step Response")
  dut.s_axis_fir_tdata.value = 1
  dut.s_axis_fir_tvalid.value = 1
  await ClockCycles(dut.clk, 50)
  dut._log.info(f'Final value after step response should be the sum of all tap values. In this case 3 + 2 + 1 + 1 + 2 + 3 = 12\nwhich is 00000001100 in binary')
  dut._log.info(f'expected output value: 00000001100 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000001100'), 'step response wrong'
  dut._log.info(f'final step response value correct!')
