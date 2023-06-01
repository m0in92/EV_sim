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
vehicle database grows. The various source for the vehicle parameters are also cited (see Reference section for details).
Please note that certain approximations and assumptions were made for the vehicle parameters. Feel free to contact the
author for more details, corrections, and/or contributions.

1. Chevy Volt 2017<sup>2</sup> : Volt_2017
2. Tesla Model 3 RWD 2023: Tesla_3_2023
    - Battery specs <sup>7,8</sup>
    - General Vehicle specs <sup>9,10,11</sup>
    - Motor specs <sup>11</sup>
3. Tesla Model S 2021-2023 : Tesla_S_2023_LongRange
   - Motor specs <sup>3</sup>
   - Battery specs <sup>4</sup>
   - General vehicle specs <sup>5,6</sup>
   - Drivetrain specs <sup>3</sup>
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
2. Plett, G. (2015). Simulating Battery Packs. In Battery Management Systems, vol 2 (1st Editio, pp. 31–67). Artech House.
3. https://www.talkingtrendo.com/tesla-model-s-electric-car/
4. https://www.qnovo.com/blogs/peek-inside-the-battery-of-a-tesla-model-s#:~:text=Panasonic%20specifies%20a%20weight%20of,kg%20or%20about%20700%20lbs.
5. https://www.caranddriver.com/features/a15108689/drag-queens-aerodynamics-compared-comparison-test/
6. https://www.tesla.com/ownersmanual/models/en_us/GUID-E414862C-CFA1-4A0B-9548-BE21C32CAA58.html
7. https://insideevs.com/news/542064/tesla-model3-lfp-battery-pack/
8. https://en.wikipedia.org/wiki/Tesla_Model_3#:~:text=The%20battery%20uses%202170%2Dsize,in%2096%20groups%20of%2031.
9. https://www.tesla.com/ownersmanual/model3/en_us/GUID-877ACE2D-B62F-4596-A6AD-A74F7905741C.html
10. https://arstechnica.com/cars/2019/03/the-tesla-model-3-reviewed-finally/#:~:text=The%20shape%20has%20purpose%2C%20though,original%20target%20of%20just%200.21.
11. https://teslamotorsclub.com/tmc/threads/model-3-frontal-area.94907/
12. https://www.researchgate.net/publication/370553199_Comparison_of_Electric_EV_and_Fossil_Fuel_Gasoline-Diesel_Vehicles_in_Terms_of_Torque_and_Power/figures?lo=1
