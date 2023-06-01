import numpy as np
import pandas as pd

from EV_sim.config import definations


class ACInductionMotor:
    def __init__(self, motor_type, rpm_r, rpm_max, l_max, eff, i):
        # check for the input motor type. np.isnan is possible in case of empty field in the EV_dataset.csv
        if isinstance(motor_type, str) or np.isnan(motor_type):
            if isinstance(motor_type, str):
                self.motor_type = motor_type
            else:
                self.motor_type = "Unknown" # set instance's motor type in case it is missing
        else:
            raise TypeError("Motor type needs to be a string or np.nan (in case it is unknown) type.")

        if isinstance(rpm_r, float):
            self.RPM_r = rpm_r # rated motor speed, rpm
        else:
            raise TypeError("Rated motor speed needs to be a float.")

        if isinstance(rpm_max, float):
            self.RPM_max = rpm_max # max motor speed, rpm
        else:
            raise TypeError("Max. motor speed needs to be a float.")

        if isinstance(l_max, float):
            self.L_max = l_max # max. torque in Nm
        else:
            raise TypeError("Max. motor torque needs to be a float.")

        if isinstance(eff, float):
            self.eff = eff # motor efficiency, unit-less
        else:
            raise TypeError("Motor efficiency needs to be a float.")

        if isinstance(i, float):
            self.I = i # motor inertia, kg m^2
        else:
            raise TypeError("Motor efficiency needs to be a float.")

        self.P_max = 2 * np.pi * self.L_max * self.RPM_r / 60000 # max motor power, kW


class Wheel:
    def __init__(self, r, i):
        if isinstance(r, float):
            self.r = r # wheel radius in m
        else:
            raise TypeError("Wheel radius needs to be a float.")

        if isinstance(i, float):
            self.I = i # wheel inertia, kg m^2
        else:
            raise TypeError("Wheel inertia needs to be a float.")


class Gearbox:
    def __init__(self, ratio, i):
        if isinstance(ratio, float):
            self.N = ratio # gearbox ratio
        else:
            raise TypeError("Gearbox ratio needs to be a float.")

        if isinstance(i, float):
            self.I = i # gearbox inertia, kg m^2
        else:
            raise TypeError("Gearbox inertia needs to be a float.")


class DriveTrain:
    def __init__(self, wheel_radius, wheel_inertia, num_wheel,
                 gearbox_ratio, gearbox_inertia,
                 inverter_eff, frac_regen_torque, eff):
        self.wheel = Wheel(r=wheel_radius, i= wheel_inertia) # Wheel object

        if isinstance(num_wheel, int):
            self.num_wheel = num_wheel # total number of wheels
        else:
            raise TypeError("Number of wheels needs to an integer.")

        self.gear_box = Gearbox(ratio=gearbox_ratio, i=gearbox_inertia) # Gearbox object

        if isinstance(inverter_eff, float):
            self.inverter_eff = inverter_eff # inverter efficiency, unit-less
        else:
            raise TypeError("Inverter efficiency needs to be a float.")

        if isinstance(frac_regen_torque, float):
            self.frac_regen_torque = frac_regen_torque # fraction of regeneration torque, unit-less
        else:
            raise TypeError("Frac_regen_torque needs to be a float.")

        if isinstance(eff, float):
            self.eff = eff # drivetrain efficiency, unit-less
        else:
            raise TypeError("Drivetrain efficiency needs to be a float.")


class BatteryCell:
    def __init__(self, manufacturer, cap, mass, v_max, v_nom, v_min, chem):
        # check for the input manufacturer type. np.isnan is possible in case of empty field in the EV_dataset.csv
        if isinstance(manufacturer, str) or np.isnan(manufacturer):
            if isinstance(manufacturer, str):
                self.cell_manufacturer = manufacturer
            else:
                self.cell_manufacturer = "Unknown" # sets the instance value in case of unknown values.
        else:
            raise TypeError("Battery cell manufacturer needs to be a string or np.nan type.")

        self.cell_cap = cap  # Battery cell capacity, A hr
        self.cell_mass = mass  # Battery cell mass, g
        self.cell_V_max = v_max  # Battery cell max. voltage, V
        self.cell_V_nom = v_nom # Battery cell nominal voltage, V
        self.cell_V_min = v_min  # Battery cell min. voltage, V

        if isinstance(chem, str) or np.isnan(chem):
            if isinstance(chem, str):
                self.cell_chem = chem # Battery cell postive electrode chemistry
            else:
                self.cell_chem = "Unknown"
        else:
            raise TypeError("Cell chemistry needs to be a string or a np.nan type.")

        self.cell_energy = self.cell_V_nom * self.cell_cap # Battery cell energy, W hr
        self.cell_spec_energy = 1000 * self.cell_energy / self.cell_mass # Battery cell specific energy, W hr/kg


class BatteryModule(BatteryCell):
    def __init__(self, cell_manufacturer, cell_cap, cell_mass, cell_v_max, cell_v_nom, cell_v_min, cell_chem,
                 n_s, n_p, overload_mass):
        super().__init__(manufacturer=cell_manufacturer, cap=cell_cap, mass=cell_mass, v_max=cell_v_max,
                         v_nom=cell_v_nom, v_min=cell_v_min, chem=cell_chem)
        self.Ns = n_s # no. of series connections of cells in a module, unit-less
        self.Np = n_p  # no. of parallel connections of cells in a module, unit-less
        self.module_overhead_mass = overload_mass  # mass beyond cell mass, percent

        self.total_no_cells = self.Ns * self.Np
        self.module_cap = self.Np * self.cell_cap  # Battery module capacity,  A hr
        self.module_mass = self.total_no_cells * (self.cell_mass / 1000) / (1 - self.module_overhead_mass)  # Battery module mass, kg
        self.module_energy = self.total_no_cells * self.cell_energy / 1000  # Battery module energy, kWh
        self.module_specific_energy = self.module_energy * 1000 / self.module_mass  # Specific energy, Wh/kg


class BatteryPack(BatteryModule):
    def __init__(self, cell_manufacturer, cell_cap, cell_mass, cell_v_max, cell_v_nom, cell_v_min, cell_chem,
                 n_s, n_p, module_overhead_mass,
                 num_modules, pack_overhead_mass, soc_full, soc_empty, eff):
        super().__init__(cell_manufacturer=cell_manufacturer, cell_cap=cell_cap, cell_mass=cell_mass, cell_v_max=cell_v_max,
                         cell_v_nom=cell_v_nom, cell_v_min=cell_v_min, cell_chem=cell_chem,
                         n_s=n_s, n_p=n_p, overload_mass=module_overhead_mass)
        self.num_modules = num_modules  # no. of modules in series, unit-less
        self.pack_overhead_mass = pack_overhead_mass  # mass beyond module and cell masses, percent
        self.SOC_full = soc_full  # Battery pack state-of-charge when full, percent
        self.SOC_empty = soc_empty  # Battery pack state-of-charge when empty, percent
        self.eff = eff  # battery pack efficiency

        self.total_no_cells = self.total_no_cells * self.num_modules  # total no. of battery cells in the pack, unit-less
        self.pack_mass = self.module_mass * self.num_modules / (1 - self.pack_overhead_mass)  # Battery pack mass, kg
        self.pack_energy = self.module_energy * self.num_modules  # Battery pack energy, Wh
        self.pack_specific_energy = self.pack_energy * 1000 / self.pack_mass  # Battery pack specific energy, Wh/kg
        self.pack_V_max = self.num_modules * self.Ns * self.cell_V_max # Battery pack max. voltage, V
        self.pack_V_nom = self.num_modules * self.Ns * self.cell_V_nom # Battery pack nominal voltage, V
        self.pack_V_min = self.num_modules * self.Ns * self.cell_V_min # battery pack min. voltage, V


class EV:
    """
    EV class contains stores all relevant vehicle parameters (e.g., wheel, drivetrain, battery pack, etc.,) as its
    class attributes. Furthermore, its has various vehicle methods to calculate for additional vehicle parameters.
    "../EV_sim/data/EV/EV_dataset.csv"
    """
    def __init__(self, alias_name: str, database_dir: str = definations.ROOT_DIR + "/data/EV/EV_dataset.csv"):
        """
        EV class constructor.
        :param alias_name: (str) Vehicle alias [i.e, identifier]
        :param database_dir: (str) The file location of the data/EV/EV_dataset.csv relative to the working directory.
        """
        self.alias_name = alias_name
        df_basicinfo = self.parse_basic_data(file_dir=database_dir)
        self.model_name = df_basicinfo["model_name"]
        self.year = df_basicinfo["year"]
        self.manufacturer = df_basicinfo["manufacturer"]
        self.trim = df_basicinfo["trim"]
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

        self.drive_train = DriveTrain(wheel_radius=wheel_radius, wheel_inertia=wheel_inertia, num_wheel=num_wheels,
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
        self.motor = ACInductionMotor(motor_type=motor_type, rpm_r=rpm_r, rpm_max=rpm_max, l_max=l_max, eff=motor_eff, i=i_motor)

        df_vehicle = self.parse_veh_info(file_dir=database_dir)
        self.C_d = float(df_vehicle["C_d"]) # drag coefficient, unit-less
        self.A_front = float(df_vehicle["frontal_area [m2]"]) # vehicle frontal area, m^2
        self.m = float(df_vehicle["mass [kg]"]) # vehicle mass, kg
        self.payload_capacity = float(df_vehicle["payload_cap [kg]"]) # vehicle payload capacity, kg
        self.overhead_power = float(df_vehicle["overhead_power [W]"]) # vehicle overhear power, W
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
        module_overhead_mass = float(df_module["overhead_mass"])
        del df_module
        df_pack = self.parse_pack_info(file_dir=database_dir)
        num_modules = int(df_pack["N_module_s"])
        pack_overhead_mass = float(df_pack["overhead_mass"])
        soc_full = float(df_pack["SOC_full"])
        soc_empty = float(df_pack["SOC_empty"])
        pack_eff = float(df_pack["eff"])
        del df_pack
        self.pack = BatteryPack(cell_manufacturer=cell_manufacturer, cell_cap=cell_cap, cell_mass=cell_mass,
                                cell_v_max=cell_v_max, cell_v_nom=cell_v_nom, cell_v_min=cell_v_min, cell_chem=cell_chem,
                                n_s=n_s, n_p=n_p, module_overhead_mass=module_overhead_mass,
                                num_modules=num_modules, pack_overhead_mass=pack_overhead_mass, soc_full=soc_full,
                                soc_empty=soc_empty, eff=pack_eff)

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

    @staticmethod
    def list_all_EV_alias(file_dir: str):
        """
        This method lists all the EV alias in the EV database.
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
