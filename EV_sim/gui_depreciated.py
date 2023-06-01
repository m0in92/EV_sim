import tkinter
from tkinter import ttk
import os
import glob

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import EV_sim
from EV_sim.config import definations


class EVSimulatorApp(tkinter.Tk):
    """
    This class displays the main dashboard of the GUI (Graphical User Interface).

    Note: Currently, the GUI only supports constant road grade and constant road force.
    """
    heading_style = ('Helvetica', 10, 'bold')

    EV_DATABASE_DIR = definations.ROOT_DIR + "/data/EV/EV_dataset.csv"
    DRIVECYCLE_FOLDER_DIR = definations.ROOT_DIR + "/data/drive_cycles/"

    def __init__(self):
        # root
        super().__init__()
        self.title('EV Simulator')
        self.iconbitmap(definations.ROOT_DIR + '/icon.ico')

        # Widget
        self.UserInputFrame = UserInput(self)
        self.ParametersFrame = Parameters(self)
        self.ResultsFrame = Results(self, var_EV_alias=self.UserInputFrame.var_EV_alias,
                                    var_dc=self.UserInputFrame.var_dc,
                                    var_air_pressure=self.UserInputFrame.var_air_pressure,
                                    var_road_grade=self.UserInputFrame.var_road_grade,
                                    var_road_force=self.UserInputFrame.var_road_force)

        # Bindings
        self.UserInputFrame.user_input_alias_combo.bind('<<ComboboxSelected>>',
                                                        self.ParametersFrame.aliasComboboxCallbackFunc)

        # mainloop
        self.mainloop()


class UserInput(ttk.Frame):
    """
    This class contains attributes and methods pertaining to the user input frame of the GUI.
    """

    # Class variables
    dc_wildcard_txt = definations.ROOT_DIR + '\data\drive_cycles\*.txt'
    all_dc = [os.path.split(file_)[-1].split('.')[0] for file_ in glob.glob(dc_wildcard_txt)] # all_dc lists all the
    # available drive cycles from drive_cycle database.

    def __init__(self, parent):
        super().__init__(parent)
        # Define variables
        self.var_EV_alias = tkinter.StringVar()  # variable for the EV alias
        self.var_dc = tkinter.StringVar()  # variable for the Drive Cycle
        self.var_air_pressure = tkinter.StringVar()  # External conditions variable
        self.var_road_grade = tkinter.StringVar()  # External conditions variable
        self.var_road_force = tkinter.StringVar()  # External conditions variable

        ttk.Label(self, text="User Input", font=EVSimulatorApp.heading_style).grid(row=0, column=0,
                                                                                   sticky=tkinter.W)  # main heading
        self.create_widgets()

        self.grid(row=0, column=0)  # placing this frame onto its parent

    def create_widgets(self):
        # subheadings
        ttk.Label(self, text="EV Alias").grid(row=1, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Drive Cycle").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Air Density, kg/m^3").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Grade, %").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Force, N").grid(row=5, column=0, sticky=tkinter.W)
        # User inputs widgets
        self.user_input_alias_combo = ttk.Combobox(self, textvariable=self.var_EV_alias)
        self.user_input_alias_combo['values'] = EV_sim.EV.list_all_EV_alias(file_dir=EVSimulatorApp.EV_DATABASE_DIR)
        user_input_dc_combo = ttk.Combobox(self, textvariable=self.var_dc)
        user_input_dc_combo['values'] = UserInput.all_dc
        ttk.Entry(self, textvariable=self.var_air_pressure).grid(row=3, column=1)
        ttk.Entry(self, textvariable=self.var_road_grade).grid(row=4, column=1)
        ttk.Entry(self, textvariable=self.var_road_force).grid(row=5, column=1)

        # Layout of wdigets
        self.user_input_alias_combo.grid(row=1, column=1)
        user_input_dc_combo.grid(row=2, column=1)


class Parameters(ttk.Frame):
    """
    This class contains attributes and methods pertaining to the Parameters frame of the GUI.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # Instance variables
        self.initiate_instance_variables()

        # Widget
        self.create_motor_frame()
        self.create_wheel_frame()
        self.create_gearbox_frame()
        self.create_dt_frame()
        self.create_cell_frame()
        self.create_module_frame()
        self.create_pack_frame()

        # Frame grid placement
        self.grid(row=0, column=1)

    def initiate_instance_variables(self):
        self.var_motor_type = tkinter.StringVar()
        self.var_motor_rated_speed = tkinter.StringVar()
        self.var_motor_max_speed = tkinter.StringVar()
        self.var_motor_max_torque = tkinter.StringVar()
        self.var_motor_eff = tkinter.StringVar()
        self.var_motor_inertia = tkinter.StringVar()
        self.var_motor_max_power = tkinter.StringVar()

        self.var_wheel_radius = tkinter.StringVar()
        self.var_wheel_inertia = tkinter.StringVar()

        self.var_gearbox_N = tkinter.StringVar()  # gearbox ratio
        self.var_gearbox_I = tkinter.StringVar()  # gearbox inertia

        self.var_dt_num_wheel = tkinter.StringVar()  # number of wheels in the vehicle
        self.var_dt_inverter_eff = tkinter.StringVar()  # inverter eff.
        self.var_dt_frac_regen_torque = tkinter.StringVar()  # fraction of regenerated torque
        self.var_dt_eff = tkinter.StringVar()  # drivetrain efficiency

        self.var_batt_cell_manu = tkinter.StringVar()
        self.var_batt_cell_cap = tkinter.StringVar()  # battery cell capacity
        self.var_batt_cell_mass = tkinter.StringVar()
        self.var_batt_cell_v_max = tkinter.StringVar()
        self.var_batt_cell_v_nom = tkinter.StringVar()
        self.var_batt_cell_v_min = tkinter.StringVar()
        self.var_batt_cell_energy = tkinter.StringVar()
        self.var_batt_cell_spec_energy = tkinter.StringVar()

        self.var_batt_module_ns = tkinter.StringVar()
        self.var_batt_module_np = tkinter.StringVar()
        self.var_batt_module_overhead_mass = tkinter.StringVar()
        self.var_tot_cells = tkinter.StringVar()
        self.var_module_cap = tkinter.StringVar()
        self.var_module_mass = tkinter.StringVar()
        self.var_module_energy = tkinter.StringVar()
        self.var_module_specific_energy = tkinter.StringVar()

        self.var_pack_num_modules = tkinter.StringVar()
        self.var_pack_mass = tkinter.StringVar()
        self.var_pack_energy = tkinter.StringVar()
        self.var_pack_specific_energy = tkinter.StringVar()
        self.var_pack_v_max = tkinter.StringVar()
        self.var_pack_v_nom = tkinter.StringVar()
        self.var_pack_v_min = tkinter.StringVar()

    def create_motor_frame(self):
        parameter_motor_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')
        motor_main_label = ttk.Label(parameter_motor_frame, text="Motor Information", font=EVSimulatorApp.heading_style)
        motor_display_label1 = ttk.Label(parameter_motor_frame, text="Motor Type")
        motor_display_label2 = ttk.Label(parameter_motor_frame, text="Rated Speed, RPM")
        motor_display_label3 = ttk.Label(parameter_motor_frame, text="Max. Speed, RPM")
        motor_display_label4 = ttk.Label(parameter_motor_frame, text="Max. Torque, Nm")
        motor_display_label5 = ttk.Label(parameter_motor_frame, text="Efficiency")
        motor_display_label6 = ttk.Label(parameter_motor_frame, text="Inertia, kg m^2")
        motor_display_label7 = ttk.Label(parameter_motor_frame, text="Max. Power, kW")

        motor_output_label1 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_type, width=20) # This
        # ttk.Label corresponds to motor type and needs extra space.
        motor_output_label2 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_rated_speed, width=10)
        motor_output_label3 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_max_speed, width=10)
        motor_output_label4 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_max_torque, width=10)
        motor_output_label5 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_eff, width=10)
        motor_output_label6 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_inertia, width=10)
        motor_output_label7 = ttk.Label(parameter_motor_frame, textvariable=self.var_motor_max_power, width=10)

        ### Motor Information
        parameter_motor_frame.grid(row=0, column=0, rowspan=2, sticky=tkinter.N)
        motor_main_label.grid(row=0, column=0)

        motor_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        motor_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        motor_display_label3.grid(row=3, column=0, sticky=tkinter.W)
        motor_display_label4.grid(row=4, column=0, sticky=tkinter.W)
        motor_display_label5.grid(row=5, column=0, sticky=tkinter.W)
        motor_display_label6.grid(row=6, column=0, sticky=tkinter.W)
        motor_display_label7.grid(row=7, column=0, sticky=tkinter.W)

        motor_output_label1.grid(row=1, column=1)
        motor_output_label2.grid(row=2, column=1)
        motor_output_label3.grid(row=3, column=1)
        motor_output_label4.grid(row=4, column=1)
        motor_output_label5.grid(row=5, column=1)
        motor_output_label6.grid(row=6, column=1)
        motor_output_label7.grid(row=7, column=1)

    def create_wheel_frame(self):
        parameter_wheel_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')
        wheel_main_label = ttk.Label(parameter_wheel_frame, text="Wheel Information", font=EVSimulatorApp.heading_style)
        wheel_display_label1 = ttk.Label(parameter_wheel_frame, text="Radius, m")
        wheel_display_label2 = ttk.Label(parameter_wheel_frame, text="Inertia, kg m^2")
        wheel_output_label1 = ttk.Label(parameter_wheel_frame, textvariable=self.var_wheel_radius, width=10)
        wheel_output_label2 = ttk.Label(parameter_wheel_frame, textvariable=self.var_wheel_inertia, width=10)

        # Grid placement
        parameter_wheel_frame.grid(row=0, column=1, sticky=(tkinter.N, tkinter.W))
        wheel_main_label.grid(row=0, column=0)
        wheel_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        wheel_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        wheel_output_label1.grid(row=1, column=1)
        wheel_output_label2.grid(row=2, column=1)

    def create_gearbox_frame(self):
        parameter_gearbox_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')
        gearbox_main_label = ttk.Label(parameter_gearbox_frame, text="Gearbox Information", font=EVSimulatorApp.heading_style)
        gearbox_display_label1 = ttk.Label(parameter_gearbox_frame, text="Gearbox Ratio")
        gearbox_display_label2 = ttk.Label(parameter_gearbox_frame, text="Inertia, kg m^2")
        gearbox_output_label1 = ttk.Label(parameter_gearbox_frame, textvariable=self.var_gearbox_N, width=10)
        gearbox_output_label2 = ttk.Label(parameter_gearbox_frame, textvariable=self.var_gearbox_I, width=10)

        # grid placement
        parameter_gearbox_frame.grid(row=1, column=1, sticky=(tkinter.N,tkinter.W))
        gearbox_main_label.grid(row=0, column=0)
        gearbox_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        gearbox_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        gearbox_output_label1.grid(row=1, column=1)
        gearbox_output_label2.grid(row=2, column=1)

    def create_dt_frame(self):
        parameter_dt_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')

        dt_main_label = ttk.Label(parameter_dt_frame, text="Drivetrain Information", font=EVSimulatorApp.heading_style)

        dt_display_label1 = ttk.Label(parameter_dt_frame, text="No. wheels")
        dt_display_label2 = ttk.Label(parameter_dt_frame, text="inverter Efficiency")
        dt_display_label3 = ttk.Label(parameter_dt_frame, text="Fraction of regeneration")
        dt_display_label4 = ttk.Label(parameter_dt_frame, text="Efficiency")

        dt_output_label1 = ttk.Label(parameter_dt_frame, textvariable=self.var_dt_num_wheel, width=10)
        dt_output_label2 = ttk.Label(parameter_dt_frame, textvariable=self.var_dt_inverter_eff, width=10)
        dt_output_label3 = ttk.Label(parameter_dt_frame, textvariable=self.var_dt_frac_regen_torque, width=10)
        dt_output_label4 = ttk.Label(parameter_dt_frame, textvariable=self.var_dt_eff, width=10)

        # Grid placement
        parameter_dt_frame.grid(row=0, column=2, sticky=(tkinter.NW))
        dt_main_label.grid(row=0, column=0)
        dt_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        dt_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        dt_display_label3.grid(row=3, column=0, sticky=tkinter.W)
        dt_display_label4.grid(row=4, column=0, sticky=tkinter.W)
        dt_output_label1.grid(row=1, column=1)
        dt_output_label2.grid(row=2, column=1)
        dt_output_label3.grid(row=3, column=1)
        dt_output_label4.grid(row=4, column=1)

    def create_cell_frame(self):
        parameter_batt_cell_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')

        battery_cell_main_label = ttk.Label(parameter_batt_cell_frame, text="Battery Cell Information",
                                            font=EVSimulatorApp.heading_style)

        battery_cell_display_label1 = ttk.Label(parameter_batt_cell_frame, text="Cell Manufacturer")
        battery_cell_display_label2 = ttk.Label(parameter_batt_cell_frame, text="Cell Capacity, Ah")
        battery_cell_display_label3 = ttk.Label(parameter_batt_cell_frame, text="Cell Mass, g")
        battery_cell_display_label4 = ttk.Label(parameter_batt_cell_frame, text="V. min., V")
        battery_cell_display_label5 = ttk.Label(parameter_batt_cell_frame, text="V. nom, V")
        battery_cell_display_label6 = ttk.Label(parameter_batt_cell_frame, text="V. min, V")
        battery_cell_display_label7 = ttk.Label(parameter_batt_cell_frame, text="Cell Energy, Wh")
        battery_cell_display_label8 = ttk.Label(parameter_batt_cell_frame, text="Cell Specific Energy, Wh/kg")

        battery_cell_output_label1 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_manu,
                                               width=10)
        battery_cell_output_label2 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_cap,
                                               width=10)
        battery_cell_output_label3 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_mass,
                                               width=10)
        battery_cell_output_label4 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_v_min,
                                               width=10)
        battery_cell_output_label5 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_v_nom,
                                               width=10)
        battery_cell_output_label6 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_v_max,
                                               width=10)
        battery_cell_output_label7 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_energy,
                                               width=10)
        battery_cell_output_label8 = ttk.Label(parameter_batt_cell_frame, textvariable=self.var_batt_cell_spec_energy,
                                               width=10)

        # Grid Placement
        parameter_batt_cell_frame.grid(row=2, column=0)
        battery_cell_main_label.grid(row=0, column=0)
        battery_cell_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        battery_cell_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        battery_cell_display_label3.grid(row=3, column=0, sticky=tkinter.W)
        battery_cell_display_label4.grid(row=4, column=0, sticky=tkinter.W)
        battery_cell_display_label5.grid(row=5, column=0, sticky=tkinter.W)
        battery_cell_display_label6.grid(row=6, column=0, sticky=tkinter.W)
        battery_cell_display_label7.grid(row=7, column=0, sticky=tkinter.W)
        battery_cell_display_label8.grid(row=8, column=0, sticky=tkinter.W)
        battery_cell_output_label1.grid(row=1, column=1, sticky=tkinter.W)
        battery_cell_output_label2.grid(row=2, column=1, sticky=tkinter.W)
        battery_cell_output_label3.grid(row=3, column=1, sticky=tkinter.W)
        battery_cell_output_label4.grid(row=4, column=1, sticky=tkinter.W)
        battery_cell_output_label5.grid(row=5, column=1, sticky=tkinter.W)
        battery_cell_output_label6.grid(row=6, column=1, sticky=tkinter.W)
        battery_cell_output_label7.grid(row=7, column=1, sticky=tkinter.W)
        battery_cell_output_label8.grid(row=8, column=1, sticky=tkinter.W)

    def create_module_frame(self):
        parameter_module_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')
        module_main_label = ttk.Label(parameter_module_frame, text="Battery Module Information",
                                      font=EVSimulatorApp.heading_style)
        module_display_label1 = ttk.Label(parameter_module_frame, text="Ns")
        module_display_label2 = ttk.Label(parameter_module_frame, text="Np")
        module_display_label3 = ttk.Label(parameter_module_frame, text="Overhead Mass, %")
        module_display_label4 = ttk.Label(parameter_module_frame, text="Tot. cells")
        module_display_label5 = ttk.Label(parameter_module_frame, text="Capacity, Ah")
        module_display_label6 = ttk.Label(parameter_module_frame, text="Mass, kg")
        module_display_label7 = ttk.Label(parameter_module_frame, text="Energy, Whr")
        module_display_label8 = ttk.Label(parameter_module_frame, text="Specific Energy, Wh")
        module_output_label1 = ttk.Label(parameter_module_frame, textvariable=self.var_batt_module_ns, width=10)
        module_output_label2 = ttk.Label(parameter_module_frame, textvariable=self.var_batt_module_np, width=10)
        module_output_label3 = ttk.Label(parameter_module_frame, textvariable=self.var_batt_module_overhead_mass,
                                         width=10)
        module_output_label4 = ttk.Label(parameter_module_frame, textvariable=self.var_tot_cells, width=10)
        module_output_label5 = ttk.Label(parameter_module_frame, textvariable=self.var_module_cap, width=10)
        module_output_label6 = ttk.Label(parameter_module_frame, textvariable=self.var_module_mass, width=10)
        module_output_label7 = ttk.Label(parameter_module_frame, textvariable=self.var_module_energy, width=10)
        module_output_label8 = ttk.Label(parameter_module_frame, textvariable=self.var_module_specific_energy, width=10)

        # Grid placement
        parameter_module_frame.grid(row=2, column=1, sticky=tkinter.N)
        module_main_label.grid(row=0, column=0)
        module_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        module_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        module_display_label3.grid(row=3, column=0, sticky=tkinter.W)
        module_display_label4.grid(row=4, column=0, sticky=tkinter.W)
        module_display_label5.grid(row=5, column=0, sticky=tkinter.W)
        module_display_label6.grid(row=6, column=0, sticky=tkinter.W)
        module_display_label7.grid(row=7, column=0, sticky=tkinter.W)
        module_display_label8.grid(row=8, column=0, sticky=tkinter.W)

        module_output_label1.grid(row=1, column=1, sticky=tkinter.W)
        module_output_label2.grid(row=2, column=1, sticky=tkinter.W)
        module_output_label3.grid(row=3, column=1, sticky=tkinter.W)
        module_output_label4.grid(row=4, column=1, sticky=tkinter.W)
        module_output_label5.grid(row=5, column=1, sticky=tkinter.W)
        module_output_label6.grid(row=6, column=1, sticky=tkinter.W)
        module_output_label7.grid(row=7, column=1, sticky=tkinter.W)
        module_output_label8.grid(row=8, column=1, sticky=tkinter.W)

    def create_pack_frame(self):
        parameter_pack_frame = ttk.Frame(self, padding="3 3 12 12", borderwidth=2, relief='sunken')

        pack_main_label = ttk.Label(parameter_pack_frame, text="Battery Module Information",
                                    font=EVSimulatorApp.heading_style)

        pack_display_label1 = ttk.Label(parameter_pack_frame, text="Tot. Modules")
        pack_display_label2 = ttk.Label(parameter_pack_frame, text="Mass, kg")
        pack_display_label3 = ttk.Label(parameter_pack_frame, text="Energy, Wh")
        pack_display_label4 = ttk.Label(parameter_pack_frame, text="Specific Energy, Wh/kg")
        pack_display_label5 = ttk.Label(parameter_pack_frame, text="V. min., V")
        pack_display_label6 = ttk.Label(parameter_pack_frame, text="V. nom., V")
        pack_display_label7 = ttk.Label(parameter_pack_frame, text="V. max., V")

        pack_output_label1 = ttk.Label(parameter_pack_frame, textvariable=self.var_pack_num_modules, width=10)
        pack_output_label2 = ttk.Label(parameter_pack_frame, textvariable=self.var_pack_mass, width=10)
        pack_output_label3 = ttk.Label(parameter_pack_frame, textvariable=self.var_pack_energy, width=10)
        pack_output_label4 = ttk.Label(parameter_pack_frame, textvariable=self.var_module_specific_energy, width=10)
        pack_output_label5 = ttk.Label(parameter_pack_frame, textvariable=self.var_pack_v_min, width=10)
        pack_output_label6 = ttk.Label(parameter_pack_frame, textvariable=self.var_pack_v_nom, width=10)
        pack_output_label7 = ttk.Label(parameter_pack_frame, textvariable=self.var_pack_v_max, width=10)

        # Grid placement
        parameter_pack_frame.grid(row=2, column=2, sticky=tkinter.N)
        pack_main_label.grid(row=0, column=0)
        pack_display_label1.grid(row=1, column=0, sticky=tkinter.W)
        pack_display_label2.grid(row=2, column=0, sticky=tkinter.W)
        pack_display_label3.grid(row=3, column=0, sticky=tkinter.W)
        pack_display_label4.grid(row=4, column=0, sticky=tkinter.W)
        pack_display_label5.grid(row=5, column=0, sticky=tkinter.W)
        pack_display_label6.grid(row=6, column=0, sticky=tkinter.W)
        pack_display_label7.grid(row=7, column=0, sticky=tkinter.W)
        pack_output_label1.grid(row=1, column=1, sticky=tkinter.W)
        pack_output_label2.grid(row=2, column=1, sticky=tkinter.W)
        pack_output_label3.grid(row=3, column=1, sticky=tkinter.W)
        pack_output_label4.grid(row=4, column=1, sticky=tkinter.W)
        pack_output_label5.grid(row=5, column=1, sticky=tkinter.W)
        pack_output_label6.grid(row=6, column=1, sticky=tkinter.W)
        pack_output_label7.grid(row=7, column=1, sticky=tkinter.W)

    def aliasComboboxCallbackFunc(self, event):
        user_input_alias_combo = event.widget.get()
        # initiate EV instance and update GUI variables
        ev_instance = EV_sim.EV(user_input_alias_combo, database_dir=EVSimulatorApp.EV_DATABASE_DIR)

        self.var_motor_type.set(ev_instance.motor.motor_type)
        self.var_motor_rated_speed.set(ev_instance.motor.RPM_r)
        self.var_motor_max_speed.set(ev_instance.motor.RPM_max)
        self.var_motor_max_torque.set(ev_instance.motor.L_max)
        self.var_motor_eff.set(ev_instance.motor.eff)
        self.var_motor_inertia.set(ev_instance.motor.I)
        self.var_motor_max_power.set(ev_instance.motor.P_max)

        self.var_wheel_radius.set(ev_instance.drive_train.wheel.r)
        self.var_wheel_inertia.set(ev_instance.drive_train.wheel.I)

        self.var_gearbox_N.set(ev_instance.drive_train.gear_box.N)
        self.var_gearbox_I.set(ev_instance.drive_train.gear_box.I)

        self.var_dt_num_wheel.set(ev_instance.drive_train.num_wheel)
        self.var_dt_inverter_eff.set(ev_instance.drive_train.inverter_eff)
        self.var_dt_frac_regen_torque.set(ev_instance.drive_train.frac_regen_torque)
        self.var_dt_eff.set(ev_instance.drive_train.eff)

        self.var_batt_cell_manu.set(ev_instance.pack.cell_manufacturer)
        self.var_batt_cell_cap.set(ev_instance.pack.cell_cap)
        self.var_batt_cell_mass.set(ev_instance.pack.cell_mass)
        self.var_batt_cell_v_min.set(ev_instance.pack.cell_V_min)
        self.var_batt_cell_v_nom.set(ev_instance.pack.cell_V_nom)
        self.var_batt_cell_v_max.set(ev_instance.pack.cell_V_max)
        self.var_batt_cell_energy.set(ev_instance.pack.cell_energy)
        self.var_batt_cell_spec_energy.set(ev_instance.pack.cell_spec_energy)

        self.var_batt_module_ns.set(ev_instance.pack.Ns)
        self.var_batt_module_np.set(ev_instance.pack.Np)
        self.var_batt_module_overhead_mass.set(ev_instance.pack.module_overhead_mass)
        self.var_tot_cells.set(ev_instance.pack.total_no_cells)
        self.var_module_cap.set(ev_instance.pack.module_cap)
        self.var_module_mass.set(ev_instance.pack.module_mass)
        self.var_module_energy.set(ev_instance.pack.module_energy)
        self.var_module_specific_energy.set(ev_instance.pack.module_specific_energy)

        self.var_pack_num_modules.set(ev_instance.pack.num_modules)
        self.var_pack_mass.set(ev_instance.pack.pack_mass)
        self.var_pack_energy.set(ev_instance.pack.pack_energy)
        self.var_pack_specific_energy.set(ev_instance.pack.pack_specific_energy)
        self.var_pack_v_max.set(ev_instance.pack.pack_V_max)
        self.var_pack_v_nom.set(ev_instance.pack.pack_V_nom)
        self.var_pack_v_min.set(ev_instance.pack.pack_V_min)


class Results(ttk.Frame):
    """
    This class contains attributes and methods pertaining to the results frame of the GUI.
    """
    error_font_style = ('Helvetica', 10, 'bold')

    def __init__(self, parent, var_EV_alias, var_dc, var_air_pressure, var_road_grade, var_road_force):
        super().__init__(parent)
        # instance variables
        self.var_EV_alias = var_EV_alias
        self.var_dc = var_dc
        self.var_air_pressure = var_air_pressure
        self.var_road_grade = var_road_grade
        self.var_road_force = var_road_force

        self.var_error_msg = tkinter.StringVar()

        # create widgets
        self.create_widgets()

        # Frame placement
        self.grid(row=1, column=0, columnspan=2)

    def create_widgets(self):
        ttk.Button(self, text="Simulate", command=self.simulate_bbt_callBackFunc).grid(row=0, column=0, columnspan=5)
        tk_canvas1 = tkinter.Canvas(self)
        tk_canvas2 = tkinter.Canvas(self)
        # tk_canvas3 = tkinter.Canvas(self)

        # create empty plots
        self.fig1 = plt.figure()  # for the first empty plot
        self.ax1 = self.fig1.add_subplot()  # for the first empty plot
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=tk_canvas1)  # for the first empty plot
        self.toolbar1 = NavigationToolbar2Tk(self.canvas1, tk_canvas1, pack_toolbar=False)

        self.fig2 = plt.figure()  # for the first empty plot
        self.ax2 = self.fig2.add_subplot()  # for the first empty plot
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=tk_canvas2)  # for the first empty plot
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, tk_canvas2, pack_toolbar=False)

        error_msg_lbl = ttk.Label(self, textvariable=self.var_error_msg, font=Results.error_font_style,
                                  foreground='red')

        # Widget placements
        tk_canvas1.grid(row=1, column=0)
        tk_canvas2.grid(row=1, column=1)
        # tk_canvas3.grid(row=1, column=2)

        self.canvas1.get_tk_widget().pack()
        self.toolbar1.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.canvas2.get_tk_widget().pack()
        self.toolbar2.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        error_msg_lbl.grid(row=2, column=0, columnspan=5)

    def simulate_bbt_callBackFunc(self):
        self.var_error_msg.set('')
        try:
            air_pressure = float(self.var_air_pressure.get())
        except:
            self.var_error_msg.set('Invalid Air Pressure.')

        try:
            road_grade = float(self.var_road_grade.get())
        except:
            self.var_error_msg.set('Invalid road grade.')

        try:
            road_force = float(self.var_road_force.get())
        except:
            self.var_error_msg.set('Invalid road force.')

        # Initialize relevant objects for the simulation
        try:
            ev_obj = EV_sim.EV(alias_name=self.var_EV_alias.get(), database_dir=EVSimulatorApp.EV_DATABASE_DIR)
        except:
            self.var_error_msg.set('Invalid EV Selection')
        try:
            dc_obj = EV_sim.DriveCycle(drive_cycle_name=self.var_dc.get(),
                                       folder_dir=EVSimulatorApp.DRIVECYCLE_FOLDER_DIR)
        except:
            self.var_error_msg.set('Invalid Drive Cycle Selection.')
        ext_cond_obj = EV_sim.ExternalConditions(rho=air_pressure, road_grade=road_grade, road_force=road_force)
        model = EV_sim.VehicleDynamics(ev_obj=ev_obj, drive_cycle_obj=dc_obj, external_condition_obj=ext_cond_obj)
        sol = model.simulate()

        # Plot the first (leftmost) figure
        self.ax1.clear()
        self.ax1.plot(dc_obj.t / 60, sol.demand_power)
        self.ax1.set_title(self.var_EV_alias.get())
        self.ax1.set_xlabel('Time [min]')
        self.ax1.set_ylabel('Battery power demand [kW]')
        self.canvas1.draw()
        self.toolbar1.update()

        # Plot the second (middle) figure
        self.ax2.clear()
        self.ax2.plot(dc_obj.t / 60, sol.current)  # the time will be in minutes
        self.ax2.set_xlabel('Time [min]')
        self.ax2.set_ylabel('Battery Current [A]')
        self.canvas2.draw()
        self.toolbar2.update()


if __name__ == '__main__':
    EVSimulatorApp()
