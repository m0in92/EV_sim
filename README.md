# EV_sim

#### Copywrite©️ 2023 by Moin Ahmed. All Rights Reserved.

<p>
This repository contains the Python source code for the simulation of power and energy demand of an electric vehicles 
(EV) during its drive cycle. This simulation takes in various vehicle parameter as its inputs. The simulation uses the
methods describes by Gillespie<sup>1</sup> and Plett<sup>2</sup>.

To summarize, the demanded motor power is calculated at every time step. This calculation is done by first calculating
the desired speed, acceleration, force, and torques. These desired variables are limited by the motor characteristics
and hence the limited torque and actual forces, acceleration, and speed are then calculated<sup>2</sup>.
</p>

### Features
- Graphic User Interface (GUI)
  - One way to execute gui is to run <code>python -m EV_sim</code> on the command line.
  
![image](Assests/gui.png)

### File Directories
- Assests: Contains images for the README.md file
- EV_Sim: Source code
- examples: example implementation using source code
- tests: Test code using the results from MATLAB code<sup>2</sup>.

### References
1. Gillespie, T. D. (Thomas D. ). (1992). Fundamentals of vehicle dynamics.
2. Plett, G. (2015). Simulating Battery Packs. In Battery Management Systems, vol 2 (1st Editio, pp. 31–67). Artech House.
