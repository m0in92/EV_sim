<div align="center">

# EV_sim
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#getting-started)

#### Copywrite©️ 2023 by Moin Ahmed. All Rights Reserved.

</div>

<div align="center">
<a href="#features"> Features </a> •
<a href="#installation"> Installation </a> •
<a href="#basic-usage"> Basic Usage </a> •
<a href="#vehicles-in-the-database"> Vehicles in the Database </a> •
<a href="#drive-cycles-in-the-package"> Drive Cycles in the Package </a> •
<a href="#file-directories"> File Directories </a> •
<a href="#how-to-cite"> How to cite </a> •
</div>

<p>
This repository contains the Python source code for simulating the power and energy demand of an electric vehicle 
(EV) during its drive cycle. This simulation takes in various vehicle parameters as its inputs. The simulation uses the 
methods described by Gillespie<sup>1</sup> and Plett<sup>2</sup>.

To summarize, the demanded motor power is calculated at every time step. This calculation is done by first calculating 
the desired speed, acceleration, force, and torques. The motor characteristics limit these desired variables, and hence 
the limited torque and actual forces, acceleration, and speed are then calculated<sup>2</sup>.

<img src="Assests/screenshot_low_quality.gif">

> If this project helps your research or product, please ⭐ star the repository and share it with peers in battery/BMS 
> communities.
> 
> Please feel free to contact the author for any questions, suggestions, and/or contributions. 
</p>



### Features
- Graphic User Interface (GUI)
  - One way to execute gui is to run <code>python -m EV_sim</code> on the command line.
  
[//]: # (![image]&#40;Assests/gui.png&#41;)

### Installation
This repository can either be used as a Python package. This package comes with a desktop GUI that can be used after
installation.

The recommended installations are listed below.

#### Git Clone 
1. Ensure Python version >= 3.10.0 is used. It is recommended to use a Python virtual environment for this project.
2. External Python dependencies can be installed on your system or Python virtual environment using the following 
command <code>pip install -r requirements.txt</code>.
3. Clone the repository, for example using <code>git clone git@github.com:m0in92/EV_sim.git</code> using Git Bash.
4. Run an example in the examples folder to test the installation. Alternatively, the gui version can be opened using
the command <code>python -m EV_sim</code> on the command line. Furthermore, included unit tests can be run to test the 
installation using the command <code>pytest tests</code> on the commandline/terminal from the project root directory.


### Basic Usage
#### Using Source code
_Note: More examples are available in the "examples" folder within the "EV_Sim" source code directory._
<p>
Import the EV_sim module using Python's import command, and this imports relevant submodules within EV_sim.

<code>import EV_sim</code>

Simulation requires instances of three classes: 
1. EV
2. DriveCycle
3. ExternalConditions

Then, "EV" class object needs to be initialized. Various vehicle parameters need to be defined to initialize it. Instead,
EV_sim provides a database of commercial electric vehicles (EV), which contains all the required parameters. For the 
list of supported commercial EV, refer to the "Vehicles in the Database" section. When using the parameters from the
database, "EVfromDatabase" class object (derived child of EV class) is called instead. The "EVfromDatabase" takes the 
vehicle alias as its input parameter. In EV_sim, the vehicle alias is a string and follows the convention: 
'manufacturer_year_model name_trim'.

For example:

<code> alias_name = "Tesla_2022_Model3_RWD" </code><br>
<code> volt = EV_sim.EVFromDatabase(alias_name=alias_name) </code>


Specify the DriveCycle and ExternalConditions class objects. </br>

<code> udds = EV_sim.DriveCycle(drive_cycle_name="us06") </code> <br>
<code> waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3) </code>


Finally, declare the VehicleDynamics object and use its simulate method. 

<code> model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo) </code> <br>
<code> sol = model.simulate() </code>

</p>

#### Using GUI
<p>
One way to execute GUI is to run <code>python -m EV_sim</code> on the command line.
</p>

### Vehicles in the Database:
<p>
The following vehicles and their corresponding vehicle alias names are listed below. This list will be updated as the 
vehicle database grows. For sources of the vehicle parameters in the database, refer to the References section.
Please note that certain approximations and assumptions were made for the vehicle parameters. Feel free to contact the
author for more details, corrections, and/or contributions.

- Audi 2021 e-tron 55 quattro  : Audi_2021_e-tron 55 quattro
- Chevy 2017 Volt  : Volt_2017
- Tesla 2022 Model 3 RWD : Tesla_2022_Model3_RWD
- Tesla 2022 Model 3 Long Range AWD : Tesla_2022_Model3_LongRangeAWD
- Tesla 2022 Model 3 Performance AWD : Tesla_2022_Model3_PerformanceAWD
- Tesla 2022 Model S Plaid Tri Motor : Tesla_2022_ModelS_PlaidTriMotorAWD
- Tesla 2022 ModelS Long Range : Tesla_2022_ModelS_LongRange
- Tesla 2022 ModelX  : Tesla_2022_ModelX
- Tesla 2022 ModelX Plaid : Tesla_2022_ModelX_Plaid
- Tesla 2022 ModelY RWD : Tesla_2022_ModelY_RWD
- Tesla 2022 ModelY Long Range AWD : Tesla_2022_ModelY_LongRangeAWD
- Tesla 2022 ModelY Performance AWD : Tesla_2022_ModelY_PerformanceAWD

</p>

### Drive Cycles in the Package:
- Air Conditioning Supplemental Driving Schedule (sc03) <sup>10</sup>
- Braunschweig City Driving Cycle (bcdc) <sup>9</sup>
- Federal Test Procedure (ftp) <sup>10</sup>
- Highway Fuel Economy test (hwfet)
- New York City Cycle (nycc)
- Unified Cycle Driving Schedule (ucds) <sup>9</sup>
- US06 (us06)
- Urban Dynamometer Driving Schedule (udds)

### File Directories
- Assets: Contains images for the README.md file
- EV_Sim: Source code
  - config: path configurations 
  - examples: example implementation using source code 
  - data: datafiles for EVs and drive cycles
  - utils: utility code for timing simulation times and printing useful database information.
- tests: Test code using the results from MATLAB code<sup>2</sup>.

### How to cite:
If you use this code in your research or want to cite this code, please cite the following:

Ahmed, M. (2024). Applications of Mathematical Models for Lithium-Ion Battery Management Systems. 
University of Waterloo. https://hdl.handle.net/10012/21242

### References
1. Gillespie, T. D. (Thomas D. ). (1992). Fundamentals of vehicle dynamics.
2. Plett, G. (2015). Simulating Battery Packs. In Battery Management Systems, vol 2 (1st Edition, pp. 31–67). Artech House.
3. https://evspecifications.com
4. https://ev-database.org
5. https://insideevs.com/
6. https://www.torquenews.com/
7. https://www.guideautoweb.com/en/
8. https://www.caranddriver.com/
9. https://www.nrel.gov/transportation/drive-cycle-tool/
10. https://www.epa.gov/vehicle-and-fuel-emissions-testing/dynamometer-drive-schedules
11. https://www.batterydesign.net/
12. https://pushevs.com/2021/03/30/ncm-712-by-lg-chem-e66a-and-e78-battery-cells/
