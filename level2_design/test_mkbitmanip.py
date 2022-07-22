# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    # SRC1, SRC2, SRC3 set to some corner values for checking, can be randomized further
    mav_putvalues =  [0x0, 0x1, 0xfffffffe, 0xffffffff]

    for i in range(0,2**17-1):
        i_bin = bin(i)[2:]
        i_bin = i_bin.zfill(17)

        mav_putvalue_src1 = 0x5
        mav_putvalue_src2 = 0x6
        mav_putvalue_src3 = 0x0
        mav_putvalue_instr = int(i_bin[0:7] + "0000000000" + i_bin[7:10] + "00000" + i_bin[10:],2)

        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # testing for all valid instructions
        if(expected_mav_putvalue != "INVALID"):
            for mav_putvalue_src1 in mav_putvalues:
                for mav_putvalue_src2 in mav_putvalues:
                    for mav_putvalue_src3 in mav_putvalues:

                        # expected output from the model
                        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
                        # print("Checking valid case")
                        # driving the input transaction
                        dut.mav_putvalue_src1.value = mav_putvalue_src1
                        dut.mav_putvalue_src2.value = mav_putvalue_src2
                        dut.mav_putvalue_src3.value = mav_putvalue_src3
                        dut.EN_mav_putvalue.value = 1
                        dut.mav_putvalue_instr.value = mav_putvalue_instr
                    
                        yield Timer(1) 

                        # obtaining the output
                        dut_output = dut.mav_putvalue.value

                        # cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
                        # cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
                        
                        # comparison
                        error_message = f'Value mismatch, for inputs SRC1 = {hex(mav_putvalue_src1)}, SRC2 = {hex(mav_putvalue_src2)}, SRC3 = {hex(mav_putvalue_src3)} and INSTR = {hex(mav_putvalue_instr)}, DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
                        assert dut_output == expected_mav_putvalue, error_message
