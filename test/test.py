# Copyright 2024 Markus Häusler
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, FallingEdge, ClockCycles, RisingEdge, Join, First
from cocotb.binary import BinaryValue


@cocotb.test()
async def test_impulse_response(dut):
  dut._log.info("start testing inital impulse response")
  
  #clock config
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  #reset device
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  #generate impulse input
  dut.s_axis_fir_tdata.value = 1
  dut.s_axis_fir_tvalid.value = 1
  dut.s_set_coeffs.value = 0
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

  dut._log.info("start testing configuration of FIR taps")
  
  #clock config
  clock = Clock(dut.clk, 10, units="us") 
  cocotb.start_soon(clock.start())

  #reset device
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  #config new FIR Filter taps 
  dut._log.info('Configuring new FIR Filter taps... \n the configured taps are 3, 2, 1')
  dut.s_set_coeffs.value = 1
  await ClockCycles(dut.clk, 6)
  dut.s_axis_fir_tdata.value = 1
  await ClockCycles(dut.clk, 1)
  dut.s_axis_fir_tdata.value = 2
  await ClockCycles(dut.clk, 1)
  dut.s_axis_fir_tdata.value = 3
  dut.s_set_coeffs.value = 0
  await ClockCycles(dut.clk, 1)
  dut.s_axis_fir_tdata.value = 0
  dut._log.info('FIR Filter taps configured')
  
  #test correctness with a impulse response
  
  #generate impulse
  await ClockCycles(dut.clk, 10)
  dut.s_axis_fir_tdata.value = 1
  dut.s_axis_fir_tvalid.value = 1
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
  
  await ClockCycles(dut.clk, 10)
  
  
  dut._log.info("Testing Step Response")
  dut.s_axis_fir_tdata.value = 1
  dut.s_axis_fir_tvalid.value = 1
  await ClockCycles(dut.clk, 50)
  dut._log.info(f'Final value after step response should be the sum of all tap values. In this case 3 + 2 + 1 + 1 + 2 + 3 = 12\nwhich is 00000001100 in binary')
  dut._log.info(f'expected output value: 00000001100 -> simulated output val: {dut.m_axis_fir_tdata.value}')
  assert dut.m_axis_fir_tdata.value == BinaryValue('00000001100'), 'step response wrong'
  dut._log.info(f'final step response value correct!')
