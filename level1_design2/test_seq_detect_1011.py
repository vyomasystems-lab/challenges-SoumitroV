# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

# seq_seen, inp_bit, reset, clk

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    test_seq = [0,0,1,0,1,1,0,1,0,1,1]

    index = 0
    golden_output = [0 for i in range(0,len(test_seq)+1)]
    idle = 0
    seq1 = 1
    seq10 = 2
    seq101 = 3
    seq1011 = 4
    curr_state = idle;
    state_tracker = [idle for i in range(0,len(test_seq)+1)]

    while(index < len(test_seq)):

        if(curr_state == idle):
            curr_state = seq1 if(test_seq[index] == 1) else idle
        
        elif(curr_state == seq1):
            curr_state = seq10 if(test_seq[index] == 0) else seq1

        elif(curr_state == seq10):
            curr_state = seq101 if(test_seq[index] == 1) else idle

        elif(curr_state == seq101):
            if(test_seq[index] == 1):
                golden_output[index+1] = 1
                curr_state = seq1011
            else :
                curr_state = idle
        
        elif(curr_state == seq1011):
            curr_state = seq1 if(test_seq[index] == 1) else idle

        state_tracker[index+1] = curr_state
        index += 1;

    for i in range(0,len(test_seq)):
        await FallingEdge(dut.clk)
        dut.inp_bit.value = test_seq[i]
        assert dut.current_state.value == state_tracker[i], "Test failed for input sequence = {test} giving state = {value} when expected state is = {exp}".format(test = test_seq[0:i+1], value = dut.current_state.value, exp = state_tracker[i])
        assert dut.seq_seen.value == golden_output[i], "Test failed for input sequence = {test} giving output = {value} when expected output is = {exp}".format(test = test_seq[0:i+1], value = dut.seq_seen.value, exp = golden_output[i])

    cocotb.log.info('#### CTB: Develop your test here! ######')
