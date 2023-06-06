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

### Usage
#### Using Source code
<p>
Import the EV_sim module using Python's import command, and this imports relevant submodules within EV_sim.

<code>import EV_sim</code>

Then, specify the EV class object whose parameters include the EV's alias name. For the list of support EV parameters, refer
to the "Vehicles in the Database" section. For example:

<code> alias_name = "Volt_2017" </code><br>
<code> volt = EV_sim.EV(alias_name=alias_name) </code>

Specify the DriveCycle and ExternalConditions class objects.

<code> udds = EV_sim.DriveCycle(drive_cycle_name="us06") </code> <br>
<code> waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3) </code>

Finally, declare the VehicleDynamics object and use it's simulate method. 

<code> model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo) </code> <br>
<code> sol = model.simulate() </code>

</p>

#### Using GUI
<p>
One way to execute gui is to run <code>python -m EV_sim</code> on the command line.
</p>

### Vehicles in the Database:
<p>
The following vehicles and their corresponding vehicle alias names are listed below. This list will be updated as the 
vehicle database grows. For sources of the vehicle parameters in the database, refer to the References section.
Please note that certain approximations and assumptions were made for the vehicle parameters. Feel free to contact the
author for more details, corrections, and/or contributions.

1. Chevy Volt 2017: Volt_2017
2. Tesla Model 3 RWD 2022: Tesla_2022_Model3_RWD
3. Tesla Model 3 Long Range: Tesla_2022_Model3_LongRangeAWD
4. Tesla Model 3 Performance: Tesla_2022_Model3_PerformanceAWD
</p>

### File Directories
- Assests: Contains images for the README.md file
- EV_Sim: Source code
  - config: path configurations 
  - examples: example implementation using source code 
  - data: datafiles for EVs and dirvecycles
- tests: Test code using the results from MATLAB code<sup>2</sup>.

### References
1. Gillespie, T. D. (Thomas D. ). (1992). Fundamentals of vehicle dynamics.
2. Plett, G. (2015). Simulating Battery Packs. In Battery Management Systems, vol 2 (1st Edition, pp. 31–67). Artech House.
3. https://evspecifications.com
4. https://ev_database.org
