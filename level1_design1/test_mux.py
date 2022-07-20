# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

# sel,inp0, inp1, inp2, inp3, inp4, inp5, inp6, inp7, inp8, 
# inp9, inp10, inp11, inp12, inp13, inp14, inp15, inp16, inp17,
# inp18, inp19, inp20, inp21, inp22, inp23, inp24, inp25, inp26,
# inp27, inp28, inp29, inp30, out

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    for i in range(0,31):
        input_sim = [1 for j in range(0,31)];
        input_sim[i] += 1

        dut.sel.value = i
        dut.inp0.value = input_sim[0]
        dut.inp1.value = input_sim[1]
        dut.inp2.value = input_sim[2]
        dut.inp3.value = input_sim[3]
        dut.inp4.value = input_sim[4]
        dut.inp5.value = input_sim[5]
        dut.inp6.value = input_sim[6]
        dut.inp7.value = input_sim[7]
        dut.inp8.value = input_sim[8]
        dut.inp9.value = input_sim[9]
        dut.inp10.value = input_sim[10]
        dut.inp11.value = input_sim[11]
        dut.inp12.value = input_sim[12]
        dut.inp13.value = input_sim[13]
        dut.inp14.value = input_sim[14]
        dut.inp15.value = input_sim[15]
        dut.inp16.value = input_sim[16]
        dut.inp17.value = input_sim[17]
        dut.inp18.value = input_sim[18]
        dut.inp19.value = input_sim[19]
        dut.inp20.value = input_sim[20]
        dut.inp21.value = input_sim[21]
        dut.inp22.value = input_sim[22]
        dut.inp23.value = input_sim[23]
        dut.inp24.value = input_sim[24]
        dut.inp25.value = input_sim[25]
        dut.inp26.value = input_sim[26]
        dut.inp27.value = input_sim[27]
        dut.inp28.value = input_sim[28]
        dut.inp29.value = input_sim[29]
        dut.inp30.value = input_sim[30]
        
        await Timer(2, units = 'ns')

        assert dut.out.value == 2, "Test failed for sel = {sel}".format(sel = i)
        # print("Test completed " + str(i+1) + " times")


    cocotb.log.info('##### CTB: Develop your test here ########')
