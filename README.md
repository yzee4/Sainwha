<p align="center">
  <img src="https://img.shields.io/badge/Sain-Wha-green?colorA=%23000000&colorB=%23006400&style=flat_square" style="width:600px;height:150px;">
</p>

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

How it works is simple, the tool sends deauthentication
packets to the network. Connected clients are deauthenticated and 
cannot be reconnected unless the attack is stopped.

<p align="center">
  <img src="docs/Sainwha-1.png" alt="Sainwha">
</p>

> Its interface is user-friendly and simple to understand.

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

# Installation

Currently Sainwha ```only supports Linux```, and will probably continue to do so. Sainwha ```supports any Linux distribution```. Installation depends only on the terminal.
> Open Linux terminal
```terminal
git clone https://github.com/yzee4/Sainwha.git
```

<h4></h4>

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Attack_Example-black?style=flat_square" style="width:300px;height:60px;">
</p>

> This is an example of a deauthentication attack on a network

<p align="center" style="text-align: center;">
  <img src="docs/Sainwha-2.png" alt="Sainwha">
</p>

First we define the scanning interface, then we check and configure the network to attack. The attack is launched and clients are disconnected until the attack is stopped.

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

# Running
After installation, just run the program
> Open Linux terminal

1. Go to Sainwha folder
```terminal
cd Sainwha
```
2. Run with Python3
```terminal
python3 sainwha.py
```

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

<h4></h4>

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/Instructions-black?style=flat_square" style="width:225px;height:60px;">
</p>

As it is an easy-to-use tool, the options are simple and easy to understand. The variables that need to be set are just ```Interface``` with ```set interface``` or just ```int```, and ```Network``` with ```set network``` or just ```net```.

<p align="center">
  <img src="docs/Sainwha-3.png" alt="Sainwha">
</p>

This menu can be opened within the tool with ```help```.

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

# Requirements

> All requirements can be installed directly on the terminal

   - `Python3` For running tool. To install use `sudo apt install python3`
   - `Git` For install tool. To install use `sudo apt install git`
   - `Aircrack-ng` For scans all networks and sends deauthentication packets. To  install use `sudo apt install aircrack-ng`
   - `Net-tools` For set interface to scans. To install use `sudo apt install net-tools`

<h1></h1>

<p align="center" style="text-align: center;">
  <img src="https://img.shields.io/badge/ -gray?style=flat_square" style="width:1000px;height:5px;">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Thanks for using-black?style=flat_square" style="width:300px;height:60px;">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Author-yzee4-green?colorA=%23000000&colorB=%23006400&style=flat_square" style="width:150px;height:30px;">
  <img src="https://img.shields.io/badge/License-MIT-green?colorA=%23000000&colorB=%23006400&style=flat_square" style="width:150px;height:30px;">
</p>
