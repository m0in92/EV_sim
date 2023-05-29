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

### Installation
Recommended installation steps are listed as follows:
1. Ensure numpy (https://numpy.org/), pandas (https://pandas.pydata.org/), and Matplotlib (https://matplotlib.org/) are installed in your system.
2. Clone the repository, for example using <code>git clone git@github.com:m0in92/EV_sim.git</code> using Git Bash.

### Vehicles in the Database:
The following vehicles and their corresponding vehicle alias names are listed below. This list will be updated as the 
vehicle database grows. The various source for the vehicle parameters are also cited (see Reference section for details).
Please note that certain approximations and assumptions were made for the vehicle parameters. Feel free to contact the
author for more details, corrections, and/or contributions.

1. Chevy Volt 2017<sup>2</sup> : Volt_2017
2. Tesla Model S 2021-2023 : Tesla_S_2023_LongRange
   - Motor specs <sup>3</sup>
   - Battery specs <sup>4</sup>
   - General Vehicle specs <sup>5,6</sup>
   - Drivetrain specs <sup>3</sup>

### File Directories
- Assests: Contains images for the README.md file
- EV_Sim: Source code
- examples: example implementation using source code
- tests: Test code using the results from MATLAB code<sup>2</sup>.

### References
1. Gillespie, T. D. (Thomas D. ). (1992). Fundamentals of vehicle dynamics.
2. Plett, G. (2015). Simulating Battery Packs. In Battery Management Systems, vol 2 (1st Editio, pp. 31–67). Artech House.
3. https://www.talkingtrendo.com/tesla-model-s-electric-car/
4. https://www.qnovo.com/blogs/peek-inside-the-battery-of-a-tesla-model-s#:~:text=Panasonic%20specifies%20a%20weight%20of,kg%20or%20about%20700%20lbs.
5. https://www.caranddriver.com/features/a15108689/drag-queens-aerodynamics-compared-comparison-test/
6. https://www.tesla.com/ownersmanual/models/en_us/GUID-E414862C-CFA1-4A0B-9548-BE21C32CAA58.html
