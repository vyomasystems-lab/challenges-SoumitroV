# Capture The Bug Hackathon
## Table of Contents
- [Introduction](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#introduction)
- [Level-1 Design-1 Multiplexer](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#level-1-design-1-multiplexer)
- [Level-1 Design-2 Sequence Detector](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#level-1-design-2-sequence-detector)
- [Level-2 Design-1 Bitmanipulation Coprocessor](https://github.com/vyomasystems-lab/challenges-SoumitroV#level-2-design-1-bitmanipulation-coprocessor)
- [Level-3 Design-1 Median Filter](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#level-3-design-1-median-filter)
- [Conclusion](https://github.com/vyomasystems-lab/challenges-SoumitroV/blob/master/README.md#conclusion)
- [Author](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#author)
- [Acknowledgements](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#acknowledgements)
- [References](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#references)

## Introduction

Capture the bug hackathon presented a series of verification challenges wherein the participants had to detect hidden bugs in RTL design code using Vyoma's UpTickPro tool. This documentation presents a brief about each design followed by the tests used to reveal the bugs and the debug code statements suggested to make the designs bug free.

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180486647-61d80bc2-6fb7-4a4b-a33e-d8279b0789a0.png"  width="80%" >
</p>
<p align="center">
Fig. 1 Vyoma's UpTickPro tool environment
</p>

## Level-1 Design-1 Multiplexer

The first design was that of a 31:1 multiplexer, with 31 input lines (each 2 bit wide), 5 bit select bus and 1 output line. The block diagram of multiplexer with input and output is presented in Fig. 2. A simple test was used wherein the select signal was incremented from 5'd0 to 5'd30. The input corresponding to select signal was driven with 2'd2 and rest all inputs were driven with 2'd1. The output was tested to assert if was equal to 2'd2 for all select inputs, else the DUT was said to fail the test.

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180592066-e2d1feb6-8311-4a6e-a4f8-dcac7ae7edbb.png"  height="400" >
</p>
<p align="center">
Fig. 2 Multiplexer block diagram
</p>

### Test Scenario 1

- Test inputs sel = 5'd12, inp12 = 2'd2, inp0-inp30 except inp12 = 2'd1
- Test output out = 2'd0
- Expected output out = 2'd2

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594424-4e331691-95b4-4343-b4d6-0c1379fb21bc.png"  width="95%" >
</p>
<p align="center">
Fig. 3 Failed test output
</p>

### Debug Scenario 1

- Can be traced to line 40, where case(sel) in matched with 5'b01101 instead of 5'b01100

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594451-197b9aa2-bac9-4bed-ab46-bab7b604dca0.png"  width="30%" >
</p>
<p align="center">
Fig. 4 Buggy code
</p>

- <b>Debug Strategy:</b> Replace ```5'b01101``` with ```5'b01100``` in line 40 

### Test Scenario 2

- Test inputs sel = 5'd30, inp30 = 2'd2, inp0-inp29 = 2'd1
- Test output out = 2'd0
- Expected output out = 2'd2

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594445-cd74df70-601e-4094-b23e-1fb92a0230cd.png"  width="95%" >
</p>
<p align="center">
Fig. 5 Failed test output
</p>

### Debug Scenario 2

- Can be traced to line 58, where case 5'b11110 is missing and case(sel) is matched with default 

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594437-d2e9cc41-e704-43b1-aa98-69d76e9a0697.png"  width="30%" >
</p>
<p align="center">
Fig. 6 Buggy code
</p>

- <b>Debug Strategy:</b> Add case ```5'b11110 : out = inp30;``` to line 58 before default case


## Level-1 Design-2 Sequence Detector

The second design was that of a 1011 sequence detector that had a serial input inp_bit, reset and clock as its inputs and seq_seen as the output that goes HIGH when the 1011 sequence is detected. The detector was to also detect overlapping sequence i.e. where final bits of a non sequence can be start of another sequence. Eg. 111011 or 101011. A block diagram of DUT with inputs and outputs is presented in Fig. 7, a simple timing diagram is also shown. To test the DUT a random sequence of 0's and 1's was generated and processed using python to produce an expected seq_seen list. The DUT was driven with the test sequence and asserted every clock cycled to check if the expected seq_seen matches simulated seq_seen, else the DUT was said to fail the test.


<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180596247-342b0fcd-5da0-4d47-bbce-e3002e94807a.png"  height="300" >
</p>
<p align="center">
Fig. 7 Sequence detector block diagram
</p>


### Test Scenario 1

- Test inputs reset = 1'b1 for one clock cycle followed by inp_bit = [1,1,0,0,1,0,1,0,1,1,0] every subsequent clock
- Test output seq_seen = 1'b0 on last clock cycle
- Expected output seq_seen = 1'b1 on last clock cycle

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594500-9d61b3e1-a10a-4183-995e-70fe42a1bd79.png"  width="95%" >
</p>
<p align="center">
Fig. 8 Failed test output
</p>

### Debug Scenario 1

- Can be traced to line 65, if current_state = SEQ_101 and inp_bit = 1'b0, then next_state should be SEQ_10 not IDLE

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594498-0861ef7d-3ef3-43d0-a873-3c70067276aa.png"  width="30%" >
</p>
<p align="center">
Fig. 9 Buggy code
</p>

- <b>Debug Strategy:</b> Replace ```next_state = IDLE;``` with ```next_state = SEQ_10;``` in line 65 

### Test Scenario 2

- Test inputs reset = 1'b1 for one clock cycle followed by inp_bit = [1,1,0,1,1,1] every subsequent clock
- Test output seq_seen = 1'b0 on last clock cycle
- Expected output seq_seen = 1'b1 on last clock cycle

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594488-866d2cd8-2a6a-44e3-a128-88b745738c74.png"  width="95%" >
</p>
<p align="center">
Fig. 10 Failed test output
</p>

### Debug Scenario 2

- Can be traced to line 49, if current_state = SEQ_1 and inp_bit = 1'b1, then next_state should be SEQ_1 not IDLE

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594480-3a44e358-e276-46f7-bd24-d606305817cd.png"  width="30%" >
</p>
<p align="center">
Fig. 11 Buggy code
</p>

- <b>Debug Strategy:</b> Replace ```next_state = IDLE;``` with ```next_state = SEQ_1;``` in line 49

### Test Scenario 3

- Test inputs reset = 1'b1 for one clock cycle followed by inp_bit = [1,0,1,1,1,0,1,1,1] every subsequent clock
- Test output seq_seen = 1'b0 on last clock cycle
- Expected output seq_seen = 1'b1 on last clock cycle

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594494-552cd778-d774-42d4-8f7e-c2f476533b9a.png"  width="95%" >
</p>
<p align="center">
Fig. 12 Failed test output
</p>

### Debug Scenario 3

- Not sure if this is real bug or intended in specification
- Two subsequent sequences 1011 1011 do not raise seq_seen twice but only once.
- Can be traced to line 69, if current_state = SEQ_1011 then next_state is directly set to IDLE disabling the sequence detector for one cycle

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594491-268a9128-33dc-4f2b-84ba-120af30e69d5.png"  width="30%" >
</p>
<p align="center">
Fig. 13 Buggy code
</p>

- <b>Debug Strategy:</b> In line 69 replace ```next_state = IDLE;``` with 
```
if(inp_bit == 1)
  next_state = SEQ_1;
else
  next_state = IDLE;
``` 

## Level-2 Design-1 Bitmanipulation Coprocessor

The third design was that of bitmanipulation coprocessor with four primary inputs, three operands mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3 each 32 bit wide and one 32 bit instruction bus mav_putvalue_instr. Inside the block the instruction is decoded and the three operands are processed giving a 32 bit output at mav_putvalue. Since the number of possible input combinations is huge 2^(32\*4), a constrained testing approach can be followed. Using the heuristic that the most likely bug can be present in instruction decoding or output calculation, all instructions are tested using fixed and limited values of operands. The possible set of instructions in generated using python, the instruction and operands are fed to a bitmanipulation coprocessor model written in python to generate the expected output. The output of DUT simulation is asserted for every valid instruction to be equal to the expected value, else the DUT was said to fail test. 

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180606225-3e0d4a9b-4e22-429f-a802-675eb3f55af3.png"  height="250" >
</p>
<p align="center">
Fig. 14 Bitmanipulation Coprocessor block diagram
</p>

### Test Scenario 1

- Test inputs mav_putvalue_src1 = 0x1, mav_putvalue_src2 = 0x0, mav_putvalue_src3 = 0x0 and mav_putvalue_instr = 0x40007033
- Test output mav_putvalue = 0x1
- Expected output mav_putvalue = 0x3

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594522-cf94c2f6-cfa4-4b63-a0fe-3205628a6197.png"  width="95%" >
</p>
<p align="center">
Fig. 15 Failed test output
</p>

### Debug Scenario 1

- Can be traced to line 2661, for the given mav_putvalue_instr = 32'b0100000_rs2_rs1_111_rd_0110011, the expected output is (mav_putvalue_src1 & ~mav_putvalue_src2)<<1, however the code has been written for (mav_putvalue_src1 & mav_putvalue_src2)<<1

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/181585023-ed66fa49-76ef-4c4e-a263-4e2756fa8d1f.png"  width="70%" >
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/181585031-7577ad7c-0c71-492b-bbb7-07e3e52955a3.png"  width="68%" >
</p>
<p align="center">
Fig. 16 Buggy code
</p>

- <b>Debug Strategy:</b> Replace ```x__h39889``` with ```(mav_putvalue_src1 & ~mav_putvalue_src2)<<1``` in line 2661


## Level-3 Design-1 Median Filter

The fourth design was that to be chosen by participants. A median filter was chosen for level 3, it had three 32 bit input words to tranfer twelve 8 bit sized pixel values to the core. The output is a 32 bit word that outputs four 8 bit sized pixels after processing with one clock cycle latency. The design was chosen to utilize the advantages of Vyoma's UpTick pro tool over testbenches written in verilog or VHDL. Since the testbench is written in a python environment, the image processing and matrix manipulation modules opencv and numpy can be leveraged to use. An image was fed to median filter in proper format and the output pixels were rearranged to form the filtered image. The resuling image was compared with the output from prebuilt median filter in opencv module. If they did not match then the dtu was said to fail the test. A visual test can be created by subtracting dut and software results, for a proper match the output image is full of 0's and is completely black.  

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/181292688-1dc0dd07-11e6-4fc2-9543-f8ebda901dc3.png"  height="450" >
</p>
<p align="center">
Fig. 17 Median filter architecture
</p>

### Test Scenario 1

- Test input Input image as presented in Fig. 18
- Test output DUT filtered image as presented in Fig. 18
- Expected output Software filtered image as presented in Fig. 18

<table>
  <tr>
    <td width="25%"><img src="https://user-images.githubusercontent.com/41693726/181292884-e57804af-fec4-48e8-b004-deb8d1f69a46.png"></td>
    <td width="25%"><img src="https://user-images.githubusercontent.com/41693726/181292964-ed0e3baa-a276-4ade-a5b5-1269ed0902ad.png"></td>
    <td width="25%"><img src="https://user-images.githubusercontent.com/41693726/181292983-2caad1d8-5d56-4d5f-93ea-9fedfd3d47e2.png"></td>
    <td width="25%"><img src="https://user-images.githubusercontent.com/41693726/181296962-2cf00e51-e550-4670-a21b-c97b2fd6f23a.png"></td>
  </tr>
  <tr>
    <td align="center">a) Input image</td>
    <td align="center">b) DUT filtered image</td>
    <td align="center">c) Software filtered image</td>
    <td align="center">d) Difference image</td>
  </tr>
</table>
<p align="center">
Fig. 18 Failed test output
</p>

### Debug Scenario 1
To debug the design, a small matrix 
```
[12, 31, 23, 52]
[121, 41, 41, 54]
[54, 1, 63, 41] 
```
was fed to the core and each submodule in the core was tested separately. The first one was a common network that took in twelve pixels and perfored sort for every three adjacent pixels.
- Test inputs common network input = [41, 54, 52, 63, 41, 23, 1, 41, 31, 54, 121, 12]
- Test output common network output = [52, 54, 41, 23, 41, 63, 31, 41, 1, 12, 121, 54]
- Expected output common network output = [54, 52, 41, 63, 41, 23, 41, 31, 1, 121, 54, 12]

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/181292807-918c3377-3a95-495e-ac15-f4f22ac6d793.png"  width="40%" >
</p>
<p align="center">
Fig. 19 Failed test output
</p>

- can be traced to line 376 of module node wherein the comparison has been done using ```data_b - data_a > 0```, although this is allowed in software programming languages with large data width, the data widths of pixel is 8 bit wide and subtraction of unsigned numbers is not performed properly resulting in incorrect comparison.


<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/181292783-08a2c772-3204-400e-bde8-f659d08eea51.png"  width="50%" >
</p>
<p align="center">
Fig. 20 Buggy code
</p>

- <b>Debug Strategy:</b> Replace ```data_b - data_a > 0``` with ```data_b > data_a``` in line 376

## Conclusion
This repository presents testing and debug results using Vyoma's UpTick pro tool for four RTL designs written in verilog. The hackathon provides a new perspective of testing by leveraging python language and its modules. New image processing and ML related hardware implementations can also be directly tested using this software.

## Author

Soumitro Vyapari, B.Tech(EE), Indian Institute of Technology Tirupati,  Andhra Pradesh 517506.

## Acknowledgements

- [Kunal Ghosh, Co-founder, VSD Corp. Pvt Ltd.](https://www.linkedin.com/in/kunal-ghosh-vlsisystemdesign-com-28084836?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B0xcWjpLDThSEo6S9UPO9Tw%3D%3D)
- [Lavanya J](https://www.linkedin.com/in/lavanya-jagadeeswaran/)
- [Vyoma Systems](https://vyomasystems.com/)
- [NIELIT](https://www.nielit.gov.in/)
- Hackathon community

## References

1. Miguel A. Vega-Rodr´ıguez, Juan Sanchez-P ´ erez, and Juan A. Gomez-Pulido. An fpga-based implementation for median filter meeting the realtime requirements of automated visual inspection systems. 01 2002.<br/>
2. Wikipedia contributors. [Bitonic sorter](https://en.wikipedia.org/wiki/Bitonic_sorter) — Wikipedia, the free encyclopedia, 2022.<br/>
3. [cocotb docs](https://docs.cocotb.org/en/stable/)


