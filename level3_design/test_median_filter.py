# See LICENSE.vyoma for details
import os
import random
from random import *
from pathlib import Path 

import numpy as np
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
        dut.word0.value = 0
        dut.word1.value = 0
        dut.word2.value = 0
        await FallingEdge(dut.clk)  
        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)
        dut.rst_n.value = 1
        await FallingEdge(dut.clk)
        await Timer(2, units = 'ns')

        img = np.array([[12,31,23,52,53],[121,41,41,54,34],[54,1,63,41,90],[53,34,65,65,87],[53,235,23,34,98]])
        (h,w) = np.shape(img)
        img = np.reshape(img,(h,w,1))
        img = np.concatenate((img,img,img),axis = 2)
        # img = np.load("img_np.npy")
        (height,width,_) = np.shape(img)
        img_filt = np.zeros((height,width))
        curr_row = -1
        curr_column = 0
        for i in range(1,height-1):
            for j in range(1,width-3,4):
                word2 = ""
                word2_list = []
                for k in range(-1,3):
                    word2 = word2 + bin(img[i-1][j+k][0])[2:].zfill(8)
                    word2_list += [img[i-1][j+k][0]]
                word1 = ""
                word1_list = []
                for k in range(-1,3):
                    word1 = word1 + bin(img[i][j+k][0])[2:].zfill(8)
                    word1_list += [img[i][j+k][0]]
                word0 = ""
                word0_list = []
                for k in range(-1,3):
                    word0 = word0 + bin(img[i+1][j+k][0])[2:].zfill(8)
                    word0_list += [img[i+1][j+k][0]]

                print("Pixel values input to median filter")
                print(word2_list)
                print(word1_list)
                print(word0_list)
                await RisingEdge(dut.clk)
                dut.word0.value = int(word0,2)
                dut.word1.value = int(word1,2)
                dut.word2.value = int(word2,2)

                
                await Timer(2, units = 'ns')
                print("Input to common network:")
                print([int(a) for a in [dut.x2_y1.value, dut.x2_y0.value,dut.x2_ym1.value,dut.x1_y1.value,dut.x1_y0.value,dut.x1_ym1.value,dut.x0_y1.value,dut.x0_y0.value,dut.x0_ym1.value,dut.xm1_y1.value,dut.xm1_y0.value,dut.xm1_ym1.value]])
                print("Output of common network:")
                print([int(a) for a in [dut.c3h.value,dut.c3m.value,dut.c3l.value,dut.c2h.value,dut.c2m.value,dut.c2l.value,dut.c1h.value,dut.c1m.value,dut.c1l.value,dut.c0h.value,dut.c0m.value,dut.c0l.value]])
                pixel1 = dut.pixel1.value
                pixel2 = dut.pixel2.value
                pixel3 = dut.pixel3.value
                pixel4 = dut.pixel4.value

                if(i*j !=1):
                    img_filt[curr_row,curr_column] = pixel1
                    img_filt[curr_row,curr_column+1] = pixel2
                    img_filt[curr_row,curr_column+2] = pixel3
                    img_filt[curr_row,curr_column+3] = pixel4
                    curr_column +=4
                    # print(int(pixel1), int(pixel2), int(pixel3), int(pixel4))
                
                if(j==1):
                        curr_row += 1
                        curr_column = 0
                
        # print("Total size ",curr_index)
        # np.save("img_filt_np",img_filt)
        # print((height,weight))
    # cocotb.log.info('##### CTB: Develop your test here ########')
