import pandas as pd
import numpy as np


class Basic_vehicle_info:
    def __init__(self, vehicle_name):
        self.check_typeErrors(vehicle_name)
        self.vehicle_name = vehicle_name
        df = self.__parse_basic_vehicle_info()
        self.EV_brand_name = df["name"]
        self.EV_manufacturer = df["manufacturer"]
        self.EV_year = df["year"]

    def check_typeErrors(self, var):
        # Check that the type of the vehicle_name is a string.
        if not (isinstance(var, str)):
            raise TypeError("vehicle_name should be of a string type.")

    def create_df(self, file_dir="data/EV/EV_dataset.csv"):
        df = pd.read_csv(file_dir, header=0)
        df.set_index(['Parameter Classification', 'Parameter Name'], inplace=True)
        if self.vehicle_name not in df.columns:
            raise Exception(f"{self.vehicle_name} not in EV_dataset.csv")
        return df

    def __parse_basic_vehicle_info(self):
        return self.create_df()[self.vehicle_name]["basic vehicle"]


class Cell(Basic_vehicle_info):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        df = self.parse_cell_info()
        self.cell_cap = float(df["capacity [A hr]"])  # in Ahr
        self.cell_mass = float(df["mass [g]"])  # in g
        self.cell_V_max = float(df["V_max [V]"])  # in V
        self.cell_V_nom = float(df["V_nom [V]"]) # in V
        self.cell_V_min = float(df["V_min [V]"])  # in V

        self.cell_energy = self.cell_V_nom * self.cell_cap # in Whr
        self.cell_spec_energy = 1000 * self.cell_energy / self.cell_mass # in Whr/kg

    def parse_cell_info(self):
        df = self.create_df()
        return df[self.vehicle_name]["cell"]


class Module(Cell):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        df = self.parse_module_info()
        self.Ns = int(df["Np"])  # no. of series connections of cells in a module [unitless]
        self.Np = int(df["Ns"])  # no. of parallel connections of cells in a module[unitless]
        self.module_overhead_mass = float(df["overhead_mass"])  # mass beyond cell mass [in percent]

        self.total_no_cells = self.Ns * self.Np
        self.module_cap = self.Np * self.cell_cap # in Ahr
        self.module_mass = self.total_no_cells * (self.cell_mass / 1000) / (1 - self.module_overhead_mass) # in kg
        self.module_energy = self.total_no_cells * self.cell_energy / 1000 # in kWhr
        self.module_specific_energy = self.module_energy * 1000 / self.module_mass # in Whr/kg

    def parse_module_info(self):
        df = self.create_df()
        return df[self.vehicle_name]["module"]


class Pack(Module):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        df = self.parse_pack_info()
        self.no_modules = int(df["N_module_s"])  # no. of modules in series
        self.pack_overhead_mass = float(df["overhead_mass"])  # mass beyond module and cell masses [in percent]
        self.SOC_full = float(df["SOC_full"])  # in percent
        self.SOC_empty = float(df["SOC_empty"])  # in percent
        self.pack_eff = float(df["eff"])  # ranges from 0 to 1

        self.total_no_cells = self.total_no_cells * self.no_modules # total no. of battery cells in the pack
        self.pack_mass = self.module_mass * self.no_modules / (1-self.pack_overhead_mass) # in kg
        self.pack_energy = self.module_energy * self.no_modules # in kWhr
        self.pack_specific_energy = self.pack_energy * 1000 / self.pack_mass # in Whr/kg
        self.pack_V_max = self.no_modules * self.Ns * self.cell_V_max
        self.pack_V_nom = self.no_modules * self.Ns * self.cell_V_nom
        self.pack_V_min = self.no_modules * self.Ns * self.cell_V_min

    def parse_pack_info(self):
        df = self.create_df()
        return df[self.vehicle_name]["pack"]


class Motor(Basic_vehicle_info):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        # self.vehicle_name = vehicle_name
        df = self.parse_motor_info()
        self.Lmax = float(df["Lmax [Nm]"])  # in Nm
        self.RPM_rated = float(df["RPM_rated [rpm]"])  # in rpm
        self.RPM_max = float(df["RPM_max [rpm]"])  # in rpm
        self.motor_eff = float(df["eff"])  # ranges from 0 to 1
        self.motor_inertia = float(df["inertia [kg/m2]"])  # in kg/m^2

        self.motor_max_power = 2 * np.pi * self.Lmax * self.RPM_rated / 60000 # in kW

    def parse_motor_info(self):
        df = self.create_df()
        return df[self.vehicle_name]["motor"]


class Wheel(Basic_vehicle_info):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        df = self.parse_wheel_info()
        self.wheel_radius = float(df["radius [m]"]) # in m
        self.wheel_inertia = float(df["inertia [kg/m2]"]) # in kg/m2
        self.roll_coeff = float(df["roll_coeff"]) # unitless

    def parse_wheel_info(self):
        df = self.create_df()
        return df[self.vehicle_name]["wheel"]


class Drivetrain(Pack, Motor, Wheel):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        df = self.parse_dt_info()
        self.inverter_eff = float(df["inverter_eff"])
        self.frac_regen_torque = float(df["frac_regen_torque"]) # ranges from 0 to 1
        self.gear_ratio = float(df["gear_ratio"])
        self.gear_inertia = float(df["gear_inertia [kg/m2]"])
        self.gear_eff = float(df["eff"])

        self.dt_eff = self.pack_eff * self.inverter_eff * self.motor_eff * self.gear_eff

    def parse_dt_info(self):
        return self.create_df()[self.vehicle_name]["drive train"]


class Vehicle(Drivetrain):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name)
        df = self.parse_vehicle_info()
        self.no_wheels = int(df["no_wheels"])
        self.road_force = float(df["road_force [N]"])
        self.frontal_area = float(df["frontal_area [m2]"]) # in m2
        self.C_d = float(df["C_d"])
        self.veh_mass = float(df["mass [kg]"]) # in kg
        self.payload_cap = float(df["payload_cap [kg]"]) # in kg
        self.overhead_power = float(df["overhead_power [W]"]) # in W

        self.veh_curb_mass = self.veh_mass + self.pack_mass
        self.veh_max_mass = self.veh_curb_mass + self.payload_cap
        self.veh_rot_mass = ((self.motor_inertia + self.gear_inertia) * (self.gear_ratio**2) + \
                            (self.wheel_inertia * self.no_wheels))/(self.wheel_radius**2)
        self.veh_equiv_mass = self.veh_max_mass + self.veh_rot_mass
        self.veh_max_speed = 2 * np.pi * self.wheel_radius * self.RPM_max * 60 / (1000 * self.gear_ratio) # in km/h

    def parse_vehicle_info(self):
        return self.create_df()[self.vehicle_name]["vehicle"]

    def __repr__(self):
        return f"{self.vehicle_name}, {self.pack_energy}, {self.motor_eff}, {self.wheel_radius}"

    def __str__(self):
        return f"{self.vehicle_name}"
