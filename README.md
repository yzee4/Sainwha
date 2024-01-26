<p align="center">
  <img src="https://img.shields.io/badge/Sain-Wha-green?colorA=%23000000&colorB=%23006400&style=flat_square" style="width:350px;height:90px;">
  <h1 align="center"></h1>
</p>

How it works is simple, the program sends deauthentication
packets to the network. Connected clients are deauthenticated and 
cannot be reconnected unless the attack is stopped.

<p align="center">
  <img src="docs/Sainwha-1.png" alt="Sainwha">
</p>
Its interface is user-friendly and simple to understand.

<h2>Installation</h2>

> Open Linux terminal

```terminal
git clone https://github.com/yzee4/Sainwha.git
```

<h1 align="center">Attack example</h1>

This is an ```example``` of a deauthentication attack on a network.
> Made in a controlled environment.

<p align="center" style="text-align: center;">
  <img src="docs/Sainwha-2.png" alt="Sainwha">
</p>

First we define the scanning interface, then we check and configure the network to attack. The attack is launched and clients are disconnected until the attack is stopped.

<h2>Running</h2>

> Open Linux terminal

1. Go to Sainwha folder
```terminal
cd Sainwha
```
2. Run with Python3
```terminal
python3 sainwha.py
```

<h1 align="center">Instructions</h1>

As it is an easy-to-use program, the options are simple and easy to understand. The variables that need to be set are just ```Interface``` with ```set interface``` or just ```int```, and ```Network``` with ```set network``` or just ```net```.

<p align="center">
  <img src="docs/Sainwha-3.png" alt="Sainwha">
</p>

This menu can be opened within the program with ```help```.

<h2>Requirements</h2>

> All requirements can be installed directly on the terminal

   - `Python3` For running program. To install use `sudo apt install python3`
   - `Nmap` For scans all networks and sends deauthentication packets. To  install use `sudo apt install nmap`
   - `Net-tools` For set interface to scans. To install use `sudo apt install net-tools`

<h1 align="center">Thanks for using!</h1>
<p align="center">
  <img src="https://img.shields.io/badge/Author-Yzee4-green?colorA=%23000000&colorB=%23006400&style=flat_square">
  <img src="https://img.shields.io/badge/License-MIT-green?colorA=%23000000&colorB=%23006400&style=flat_square">
</p>
