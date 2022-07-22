# Capture The Bug Hackathon
## Table of Contents
- [Introduction]
- [Level-1 Design-1 Multiplexer]
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
<img src="https://user-images.githubusercontent.com/41693726/180486647-61d80bc2-6fb7-4a4b-a33e-d8279b0789a0.png"  width="800" >
</p>
<p align="center">
Fig 1. Vyoma's UpTickPro tool environment
</p>

## Level-1 Design-1 Multiplexer

The first design was that of a 31:1 multiplexer, with 31 input lines, 4 bit select bus and 1 output line. The block diagram of multiplexer with input and output is presented in Fig. 2. 

