# See LICENSE.vyoma for details
import os
import random
from random import *
from pathlib import Path

import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge


@cocotb.test()
async def test_median_filter(dut):
    
        PERIOD = 10;
        PIXEL_DATA_WIDTH = 8;
        LUT_ADDR_WIDTH = 10; 
        MEM_ADDR_WIDTH = 10; 

        clock = Clock(dut.clk, PERIOD, units="ns")  # Create a 10us period clock on port clk
        cocotb.start_soon(clock.start())        # Start the clock

        # reset
        dut.rst_n.value = 0
        await FallingEdge(dut.clk)  
        dut.rst_n.value = 1
        await FallingEdge(dut.clk)
        await Timer(2, units = 'ns')

        img = [[12,31,23,52,53],[121,41,41,54,34],[54,1,63,41,90],[53,34,65,65,87],[53,235,23,34,98]]

        for i in range(1,4):
            for j in range(1,2):
                word0 = ""
                for k in range(-1,3):
                    word0 = word0 + bin(img[i-1][j+k])[2:].zfill(8)
                word1 = ""
                for k in range(-1,3):
                    word1 = word1 + bin(img[i][j+k])[2:].zfill(8)
                word2 = ""
                for k in range(-1,3):
                    word2 = word2 + bin(img[i+1][j+k])[2:].zfill(8)

                dut.word0.value = int(word0,2)
                dut.word1.value = int(word1,2)
                dut.word2.value = int(word2,2)

                await FallingEdge(dut.clk)
                pixel1 = dut.pixel1.value
                pixel2 = dut.pixel2.value
                pixel3 = dut.pixel3.value
                pixel4 = dut.pixel4.value

                print(int(pixel1), int(pixel2), int(pixel3), int(pixel4))
                # assert dut.out.value == 2, "Test failed for sel = {sel}, expected output = {exp_out}, incorrect output {incorrect_out}".format(sel = i, exp_out = 2, incorrect_out = dut.out.value)
                # print("Test completed " + str(i+1) + " times")


    # cocotb.log.info('##### CTB: Develop your test here ########')
