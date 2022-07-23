# Capture The Bug Hackathon
## Table of Contents
- [Introduction](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#introduction)
- [Level-1 Design-1 Multiplexer](https://github.com/vyomasystems-lab/challenges-SoumitroV/edit/master/README.md#level-1-design-1-multiplexer)
- [Level-1 Design-2 Sequence Detector]
- [Level-2 Design-1 Bitmanipulation Coprocessor]
- [Level-3 Design-1 Median Filter]
- [Conclusion]
- [Author]
- [Acknowledgements]
- [References]

## Introduction

Capture the bug hackathon presented a series of verification challenges wherein the participants had to detect hidden bugs in RTL design code using Vyoma's UpTickPro tool. This documentation presents a brief about each design followed by the tests used to reveal the bugs and the debug code statements suggested to make the designs bug free.

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180486647-61d80bc2-6fb7-4a4b-a33e-d8279b0789a0.png"  width="80%" >
</p>
<p align="center">
Fig 1. Vyoma's UpTickPro tool environment
</p>

## Level-1 Design-1 Multiplexer

The first design was that of a 31:1 multiplexer, with 31 input lines (each 2 bit wide), 5 bit select bus and 1 output line. The block diagram of multiplexer with input and output is presented in Fig. 2. A simple test was used wherein the select signal was incremented from 5'd0 to 5'd30. The input corresponding to select signal was driven with 2'd2 and rest all inputs were driven with 2'd1. The output was tested to assert if was equal to 2'd2 for all select inputs, if not then the DUT was said to fail the test.

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180592066-e2d1feb6-8311-4a6e-a4f8-dcac7ae7edbb.png"  height="400" >
</p>
<p align="center">
Fig 2. Multiplexer block diagram
</p>

### Test Scenario 1

- Test inputs sel = 5'd12, inp12 = 2'd2, inp0-inp30 except inp12 = 2'd1
- Test output out = 2'd0
- Expected output out = 2'd2

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594424-4e331691-95b4-4343-b4d6-0c1379fb21bc.png"  width="95%" >
</p>
<p align="center">
Fig 3. Failed test output
</p>

### Debug Scenario 1

- Can be traced to line 40, where case(sel) in matched with 5'b01101 instead of 5'b01100

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594451-197b9aa2-bac9-4bed-ab46-bab7b604dca0.png"  width="30%" >
</p>
<p align="center">
Fig 4. Buggy code
</p>

- <b>Debug Strategy:</b> Replace 5'b01101 with 5'b01100 in line 40 

### Test Scenario 2

- Test inputs sel = 5'd30, inp30 = 2'd2, inp0-inp29 = 2'd1
- Test output out = 2'd0
- Expected output out = 2'd2

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594445-cd74df70-601e-4094-b23e-1fb92a0230cd.png"  width="95%" >
</p>
<p align="center">
Fig 5. Failed test output
</p>


### Debug Scenario 2

- Can be traced to line 58, where case 5'b11110 is missing and case(sel) is matched with default 

<p align="center">
<img src="https://user-images.githubusercontent.com/41693726/180594437-d2e9cc41-e704-43b1-aa98-69d76e9a0697.png"  width="30%" >
</p>
<p align="center">
Fig 6. Buggy code
</p>

- <b>Debug Strategy:</b> Add case 5'b11110 : out = inp30; to line 58 before default case

## Level-1 Design-2 Sequence Detector

