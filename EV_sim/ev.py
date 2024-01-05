"""
This module provides the classes pertaining to the parameters and functionailities of the various components of an
electric vehicle.
"""

__all__ = ['ACInductionMotor', 'Wheel', 'Gearbox', 'DriveTrain', 'BatteryCell', 'BatteryModule', 'BatteryPack', 'EV',
           'EVFromDatabase']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by EV_sim. All rights reserved."


import os
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from EV_sim.config import definations


@dataclass
class ACInductionMotor:
    motor_type: float # motor type
    RPM_r: float # rated motor speed, rpm
    RPM_max: float # max. motor speed, rpm
    L_max: float # max. torque, Nm
    eff: float # motor efficiency, unit-less
    I: float # motor inertia, kg/m2

    def __post_init__(self):
        # check for the input motor type. np.isnan is possible in case of empty field in the EV_dataset.csv
        if isinstance(self.motor_type, str) or np.isnan(self.motor_type):
            if isinstance(self.motor_type, str):
                self.motor_type = self.motor_type
            else:
                self.motor_type = "Unknown" # set instance's motor type in case it is missing
        else:
            raise TypeError("Motor type needs to be a string or np.nan (in case it is unknown) type.")

        if not isinstance(self.RPM_r, float):
            raise TypeError("Rated motor speed needs to be a float.")

        if not isinstance(self.RPM_max, float):
            raise TypeError("Max. motor speed needs to be a float.")

        if not isinstance(self.L_max, float):
            raise TypeError("Max. motor torque needs to be a float.")

        if not isinstance(self.eff, float):
            raise TypeError("Motor efficiency needs to be a float.")

        if not isinstance(self.I, float):
            raise TypeError("Motor efficiency needs to be a float.")

        self.P_max = 2 * np.pi * self.L_max * self.RPM_r / 60000 # max motor power, kW


@dataclass
class Wheel:
    r: float # wheel radius
    I: float # wheel inertia

    def __post_init__(self):
        if not isinstance(self.r, float):
            raise TypeError("Wheel radius needs to be a float.")
        if not isinstance(self.I, float):
            raise TypeError("Wheel inertia needs to be a float.")


@dataclass()
class Gearbox:
    N: float # gear box ratio
    I: float # gearbox inertia

    def __post_init__(self):
        if not isinstance(self.N, float):
            raise TypeError("Gearbox ratio needs to be a float.")
        if not isinstance(self.I, float):
            raise TypeError("Gearbox inertia needs to be a float.")


@dataclass
class DriveTrain:
    wheel_radius: int # wheel radius, m
    wheel_inertia: float # wheel inertia, kg/m2
    num_wheel: int # number of wheels in a drivetrain
    gearbox_ratio: float # gearbox ratio
    gearbox_inertia: float # gearbox inertia, kg/m2
    inverter_eff: float # inverter efficiency, unit-less
    frac_regen_torque: float # fraction of regenerated torque
    eff: float # drivetrain efficiency

    def __post_init__(self):
        self.wheel = Wheel(r= self.wheel_radius, I=self.wheel_inertia) # Wheel object
        del self.wheel_radius, self.wheel_inertia

        if not isinstance(self.num_wheel, int):
            raise TypeError("Number of wheels needs to an integer.")

        self.gear_box = Gearbox(N=self.gearbox_ratio, I=self.gearbox_inertia) # Gearbox object
        del self.gearbox_ratio, self.gearbox_inertia

        if not isinstance(self.inverter_eff, float):
            raise TypeError("Inverter efficiency needs to be a float.")

        if not isinstance(self.frac_regen_torque, float):
            raise TypeError("Frac_regen_torque needs to be a float.")

        if not isinstance(self.eff, float):
            raise TypeError("Drivetrain efficiency needs to be a float.")


@dataclass
class BatteryCell:
    cell_manufacturer: str # Battery cell manufacturer
    cell_cap: float  # Battery cell capacity, A hr
    cell_mass: float  # Battery cell mass, g
    cell_V_max: float  # Battery cell max. voltage, V
    cell_V_nom: float  # Battery cell nominal voltage, V
    cell_V_min: float  # Battery cell min. voltage, V
    cell_chem: str  # Battery positive electrode chemistry

    def __post_init__(self):
        # check for the input manufacturer type. np.isnan is possible in case of empty field in the EV_dataset.csv
        if isinstance(self.cell_manufacturer, str) or pd.isnull(self.cell_manufacturer):
            if isinstance(self.cell_manufacturer, str):
                self.cell_manufacturer = self.cell_manufacturer
            else:
                self.cell_manufacturer = "Unknown" # sets the instance value in case of unknown values.
        else:
            raise TypeError("Battery cell manufacturer needs to be a string or np.nan type.")

        if not isinstance(self.cell_cap, float):
            raise TypeError('cell_cap needs to be a float type.')
        if not isinstance(self.cell_mass, float):
            raise TypeError('cell_mass needs to be a float type.')
        if not isinstance(self.cell_V_max, float):
            raise TypeError('cell_V_max needs to be a float type.')
        if not isinstance(self.cell_V_nom, float):
            raise TypeError('cell_V_nom needs to be a float type.')
        if not isinstance(self.cell_V_min, float):
            raise TypeError('cell_V_min needs to be a float type.')

        if isinstance(self.cell_chem, str) or np.isnan(self.cell_chem):
            if isinstance(self.cell_chem, str):
                self.cell_chem = self.cell_chem # Battery cell postive electrode chemistry
            else:
                self.cell_chem = "Unknown"
        else:
            raise TypeError("Cell chemistry needs to be a string or a np.nan type.")

        self.cell_energy = self.cell_V_nom * self.cell_cap  # Battery cell energy, W hr
        self.cell_spec_energy = 1000 * self.cell_energy / self.cell_mass  # Battery cell specific energy, W hr/kg


@dataclass
class BatteryModule(BatteryCell):
    Ns: int
    Np: int
    module_overhead_mass: float

    def __post_init__(self):
        super().__post_init__()

        self.total_no_cells = self.Ns * self.Np
        self.module_cap = self.Np * self.cell_cap  # Battery module capacity,  A hr
        self.module_mass = self.total_no_cells * (self.cell_mass / 1000) / (1 - self.module_overhead_mass)  # Battery module mass, kg
        self.module_energy = self.total_no_cells * self.cell_energy / 1000  # Battery module energy, kWh
        self.module_specific_energy = self.module_energy * 1000 / self.module_mass  # Specific energy, Wh/kg


@dataclass
class BatteryPack(BatteryModule):
    num_modules: int # no. of modules in series, unit-less
    pack_overhead_mass: float # mass beyond module and cell masses, percent
    SOC_full: float # Battery pack state-of-charge when full, percent
    SOC_empty: float # Battery pack state-of-charge when empty, percent
    eff: float # battery pack efficiency

    def __post_init__(self):
        super().__post_init__()

        self.total_no_cells = self.total_no_cells * self.num_modules  # total no. of battery cells in the pack, unit-less
        self.pack_mass = self.module_mass * self.num_modules / (1 - self.pack_overhead_mass)  # Battery pack mass, kg
        self.pack_energy = self.module_energy * self.num_modules  # Battery pack energy, Wh
        self.pack_specific_energy = self.pack_energy * 1000 / self.pack_mass  # Battery pack specific energy, Wh/kg
        self.pack_V_max = self.num_modules * self.Ns * self.cell_V_max # Battery pack max. voltage, V
        self.pack_V_nom = self.num_modules * self.Ns * self.cell_V_nom # Battery pack nominal voltage, V
        self.pack_V_min = self.num_modules * self.Ns * self.cell_V_min # battery pack min. voltage, V


@dataclass
class EV:
    """
    EV stores all relevant vehicle parameters (e.g., wheel, drivetrain, battery pack, etc.,) as its class attributes.
    Furthermore, its has various vehicle methods to calculate for additional vehicle parameters.
    """
    # Basic EV information
    alias_name: Optional[str] = None
    model_name: Optional[str] = None
    year: Optional[int] = None
    manufacturer: Optional[str] = None
    trim: Optional[str] = None

    # vehicle's component class objects
    drive_train: Optional[DriveTrain] = None
    motor: Optional[ACInductionMotor] = None
    pack: Optional[BatteryPack] = None

    # Other vehicle information
    C_d: Optional[float] = None # drag coefficient, unit-less
    A_front: Optional[float] = None # vehicle frontal area, m^2
    m: Optional[float] = None # vehicle mass, kg
    payload_capacity: Optional[float] = None # vehicle payload capacity, kg
    overhead_power: Optional[float] = None # vehicle overhear power, W

    @property
    def curb_mass(self) -> float:
        """
        Vehicle curb mass in units of kg.
        :return: (float) vehicle curb mass, kg
        """
        return self.m + self.pack.pack_mass

    @property
    def max_mass(self) -> float:
        """
        Vehicle maximum mass in units of kg.
        :return: (float) vehicle maximum mass, kg
        """
        return self.curb_mass + self.payload_capacity

    @property
    def rot_mass(self) -> float:
        """
        Vehicle rotating equivalent mass in units of kg.
        :return: (float)
        """
        return ((self.motor.I + self.drive_train.gear_box.I) * (self.drive_train.gear_box.N ** 2) + \
                (self.drive_train.wheel.I * self.drive_train.num_wheel))/(self.drive_train.wheel.r ** 2)

    @property
    def equiv_mass(self) -> float:
        """
        Vehicle's equivalent mass is a sum of its maximum and translational equivalent mass of the rotating inertia.
        :return: (float) Vehicle equivalent mass, kg
        """
        return self.max_mass + self.rot_mass

    @property
    def max_speed(self) -> float:
        """
        Vehicle maximum speed in km/h
        :return: (float) Vehicle max. speed, km/h
        """
        return 2 * np.pi * self.drive_train.wheel.r * self.motor.RPM_max * 60 / (1000 * self.drive_train.gear_box.N)


class EVFromDatabase(EV):
    """
    EVFromDatabase inherits from the EV class. It is meant to update the attributes of its parent EV class using the
    Database.
    """
    def __init__(self, alias_name: str, database_dir: str = os.path.join(definations.ROOT_DIR, "data", "EV", "EV_dataset.csv")):
        """
        EV class constructor.
        :param alias_name: (str) Vehicle alias [i.e, identifier]
        :param database_dir: (str) The file location of the data/EV/EV_dataset.csv relative to the working directory.
        """
        self.alias_name = alias_name
        df_basicinfo = self.parse_basic_data(file_dir=database_dir)
        model_name = df_basicinfo["model_name"]
        year = df_basicinfo["year"]
        manufacturer = df_basicinfo["manufacturer"]
        trim = df_basicinfo["trim"]
        del df_basicinfo

        df_wheel = self.parse_wheel_info(file_dir=database_dir)
        wheel_radius = float(df_wheel["radius [m]"])
        wheel_inertia = float(df_wheel["inertia [kg/m2]"])
        self.C_r = float(df_wheel["roll_coeff"]) # rolling coefficient, unit-less
        del df_wheel

        df_drivetrain = self.parse_drivetrain_info(file_dir=database_dir)
        gearbox_ratio = float(df_drivetrain["gear_ratio"]) # motor rpm / wheel rpm, unit-less
        gearbox_inertia = float(df_drivetrain["gear_inertia [kg/m2]"])
        inverter_eff = float(df_drivetrain["inverter_eff"])
        frac_regen_torque = float(df_drivetrain["frac_regen_torque"])
        dt_eff = float(df_drivetrain["eff"])
        num_wheels = int(df_drivetrain["no_wheels"])
        del df_drivetrain

        drive_train_obj = DriveTrain(wheel_radius=wheel_radius, wheel_inertia=wheel_inertia, num_wheel=num_wheels,
                                  gearbox_ratio=gearbox_ratio, gearbox_inertia=gearbox_inertia,
                                  inverter_eff=inverter_eff, frac_regen_torque=frac_regen_torque, eff=dt_eff)

        df_motor = self.parse_motor_info(file_dir=database_dir)
        motor_type = df_motor["type"]
        rpm_r = float(df_motor["RPM_rated [rpm]"])
        rpm_max = float(df_motor["RPM_max [rpm]"])
        l_max = float(df_motor["Lmax [Nm]"])
        motor_eff = float(df_motor["eff"])
        i_motor = float(df_motor["inertia [kg/m2]"])
        del df_motor
        motor_obj = ACInductionMotor(motor_type=motor_type, RPM_r=rpm_r, RPM_max=rpm_max, L_max=l_max, eff=motor_eff,
                                 I=i_motor)

        df_vehicle = self.parse_veh_info(file_dir=database_dir)
        C_d = float(df_vehicle["C_d"]) # drag coefficient, unit-less
        A_front = float(df_vehicle["frontal_area [m2]"]) # vehicle frontal area, m^2
        m = float(df_vehicle["mass [kg]"]) # vehicle mass, kg
        payload_capacity = float(df_vehicle["payload_cap [kg]"]) # vehicle payload capacity, kg
        overhead_power = float(df_vehicle["overhead_power [W]"]) # vehicle overhear power, W
        del df_vehicle

        df_cell = self.parse_cell_info(file_dir=database_dir)
        cell_manufacturer = df_cell["battery_cell_manufacturer"]
        cell_cap = float(df_cell["capacity [A hr]"])
        cell_mass = float(df_cell["mass [g]"])
        cell_v_max = float(df_cell["V_max [V]"])
        cell_v_nom = float(df_cell["V_nom [V]"])
        cell_v_min = float(df_cell["V_min [V]"])
        cell_chem = df_cell['positive electrode chem.']
        del df_cell
        df_module = self.parse_module_info(file_dir=database_dir)
        n_s = int(df_module["Ns"])
        n_p = int(df_module["Np"])
        module_overhead_mass = float(df_module["overhead_mass [%]"])
        del df_module
        df_pack = self.parse_pack_info(file_dir=database_dir)
        num_modules = int(df_pack["N_module_s"])
        pack_overhead_mass = float(df_pack["overhead_mass [%]"])
        soc_full = float(df_pack["SOC_full"])
        soc_empty = float(df_pack["SOC_empty"])
        pack_eff = float(df_pack["eff"])
        del df_pack
        pack_obj = BatteryPack(cell_manufacturer=cell_manufacturer, cell_cap=cell_cap, cell_mass=cell_mass,
                               cell_V_max=cell_v_max, cell_V_nom=cell_v_nom, cell_V_min=cell_v_min, cell_chem=cell_chem,
                               Ns=n_s, Np=n_p, module_overhead_mass=module_overhead_mass,
                               num_modules=num_modules, pack_overhead_mass=pack_overhead_mass, SOC_full=soc_full,
                               SOC_empty=soc_empty, eff=pack_eff)

        super().__init__(alias_name=alias_name, model_name=model_name, year=year, manufacturer=manufacturer, trim=trim,
                         drive_train = drive_train_obj, motor = motor_obj, pack= pack_obj,
                         C_d=C_d, A_front=A_front, m=m, payload_capacity=payload_capacity, overhead_power=overhead_power)

    @staticmethod
    def list_all_EV_alias(file_dir: str) -> list:
        """
        Lists all the EV alias in the EV database.
        :return: (list) list of all EV alias in the EV database
        """
        df = pd.read_csv(file_dir)
        df.set_index(['Parameter Classification', 'Parameter Name'], inplace=True)
        return df.columns.tolist()

    def create_df(self, file_dir: str):
        """
        returns a dataframe containing all the relevant EV information.
        :param file_dir:
        :return:
        """
        df = pd.read_csv(file_dir, header=0)
        df.set_index(['Parameter Classification', 'Parameter Name'], inplace=True)
        if self.alias_name not in df.columns:
            raise Exception(f"{self.alias_name} not in EV dataset")
        return df[self.alias_name]

    def parse_basic_data(self, file_dir: str):
        """
        Returns a dataframe containing the basic EV information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["basic vehicle"]

    def parse_wheel_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's motor information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["wheel"]

    def parse_drivetrain_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's drive train information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["drive train"]

    def parse_motor_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's drive train information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["motor"]

    def parse_veh_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's drive train information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["vehicle"]

    def parse_cell_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's battery cell information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["cell"]

    def parse_module_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's battery module information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["module"]

    def parse_pack_info(self, file_dir: str):
        """
        Returns a dataframe containing the EV's battery pack information
        :param file_dir:
        :return:
        """
        return self.create_df(file_dir=file_dir)["pack"]

    def __repr__(self):
        return f"EV('{self.alias_name}')"

    def __str__(self):
        return f"{self.alias_name} made by {self.manufacturer}"

