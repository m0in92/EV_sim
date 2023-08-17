#  Copyright (c) 2023. Moin Ahmed. All rights reserved.

"""Graphical User Interface for Vehicle Dynamics made using Python's Tkinter."""


import glob
import os
import tkinter
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import EV_sim
from EV_sim.config import definations
from EV_sim.tkinter_gui_depreciated.menubar import MenuBarClass
from EV_sim.tkinter_gui_depreciated.sim_variables import InputSimVariables
from EV_sim.tkinter_gui_depreciated.ribbon import Ribbon

# Global variables
icon_dir = os.path.join(definations.ROOT_DIR, 'tkinter_gui', 'icon.ico')


matplotlib.use('TkAgg')


class VehicleDynamicsApp(tkinter.Tk):
    """
    Contains method and attributes for the root window. It creates the main window, menubar, panedwindow, and the
    Input and Display Frames. The main window contains the menubar and paned window. The paned window contains frames
    for inputs and display.
    """
    heading_style = ('Helvetica', 10, 'bold')
    heading_style2 = ('Helvetica', 8, 'bold')
    error_font_style = ('Helvetica', 10, 'bold')

    EV_DATABASE_DIR = definations.ROOT_DIR + "/data/EV/EV_dataset.csv"
    DRIVECYCLE_FOLDER_DIR = definations.ROOT_DIR + "/data/drive_cycles/"

    def __init__(self):
        # root/window
        super().__init__()
        self.title('EV Simulator')
        self.iconbitmap(icon_dir)
        self.geometry('1200x800')

        # instance variables
        self.var_lstbox_inputs_user_choice = tkinter.StringVar()
        self.set_two_decimal = tkinter.BooleanVar()  # option whether to show results in two decimal places.
        self.set_two_decimal.set(False)  # Initialize so that this option is False

        # Style, only for the paned window scroll
        style = ttk.Style()
        style.theme_use('classic')

        # Widgets
        mb = MenuBarClass(self)  # menubar using the MenuBarClass below.
        rib = Ribbon(self)
        self.pw = ttk.PanedWindow(self, orient=tkinter.HORIZONTAL)  # PanedWindow Widget
        self.InputAndDisplayFrame = InputAndDisplayFrames(parent=self.pw)  # Input and Display Frames Widget

        # Widget grid placements
        self.pw.grid(row=1, column=0, sticky="news")

        # Row and column configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.config(menu=mb)

        # main loop
        self.mainloop()


class InputAndDisplayFrames(ttk.Frame):
    """
    Contains the attributes and methods pertaining to the Input (that appears of the left of the gui) and Display Frames
    (that appears on the right of the gui).
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)

        # Instance variables
        self.sim_vars = InputSimVariables()

        self.var_air_pressure = tkinter.StringVar()
        self.var_road_grade = tkinter.StringVar()
        self.var_road_force = tkinter.StringVar()

        # Inputs Widgets (those that appear on the left side of the gui)
        InputsOnInputFrame(
            self)  # it is important to pass the whole parent to this class instance. This is because this
        # class instance needs to change the existing variables.
        ParametersOnInputFrame(self)  # Parameter Widgets
        ResultInput(parent=self, start_row_num=4)  # Results Widget

        # Display Widgets (those that appears on the right of the gui)
        self.fme_display = ttk.Frame(parent)  # display frame

        # Widget placement
        self.grid(row=1, column=0, rowspan=100)
        parent.add(self)
        self.fme_display.grid(row=0, column=1, sticky="news")
        parent.add(self.fme_display)


class InputsOnInputFrame(ttk.Frame):
    """
    Contains attributes and methods pertaining to the Input Frame on the Input Display.
    """
    # class variables
    lstbox_inputs_choices = ["EV", "Drive Cycle", "External Conditions"]  # all main choices in the input section

    input_display_heading1 = f"{lstbox_inputs_choices[0]}"
    input_display_heading2 = f"{lstbox_inputs_choices[1]}"
    input_display_heading3 = f"{lstbox_inputs_choices[2]}"

    def __init__(self, parent) -> None:
        """
        Class constructor
        :param parent: (InputAndDisplayFrames) InputAndDisplayFrames instance.
        """
        if isinstance(parent, InputAndDisplayFrames):
            self.parent = parent
        else:
            raise TypeError("parent needs to be InputAndDisplay Object instance.")

        super().__init__(parent)

        # Instance variables
        self.var_lstbox_inputs_choices = tkinter.StringVar()
        self.var_lstbox_inputs_choices.set(InputsOnInputFrame.lstbox_inputs_choices)

        # Widgets
        ttk.Label(self, text="Inputs", font=VehicleDynamicsApp.heading_style).grid(row=0, column=0, sticky="news")
        self.lstbox_inputs = tkinter.Listbox(self, width=50, listvariable=self.var_lstbox_inputs_choices,
                                             selectmode="single", exportselection=False,
                                             height=len(self.lstbox_inputs_choices))

        # Bindings
        self.lstbox_inputs.bind('<<ListboxSelect>>', self.set_lstbox_input_user_choice)

        # Grid layout
        self.lstbox_inputs.grid(row=1, column=0, sticky="news")
        self.grid(row=0, column=0)

    def set_lstbox_input_user_choice(self, event) -> None:
        user_choice = self.lstbox_inputs.get(self.lstbox_inputs.curselection())
        InputsDisplay(self.parent.fme_display, text=user_choice, sim_vars_instance=self.parent.sim_vars) # the parent
        # is the Inputs and Display Frame


class ParametersOnInputFrame(ttk.Frame):
    # Class variables
    lstbox_params_choices = ["Basic", "Cell", "Module", "Pack", "Motor", "Wheel", "Drivetrain", "Design"]

    params_display_heading1 = f"Vehicle {lstbox_params_choices[0]} Information"
    params_display_heading2 = f"Vehicle {lstbox_params_choices[1]} Information"
    params_display_heading3 = f"Vehicle {lstbox_params_choices[2]} Information"
    params_display_heading4 = f"Vehicle {lstbox_params_choices[3]} Information"
    params_display_heading5 = f"Vehicle {lstbox_params_choices[4]} Information"
    params_display_heading6 = f"Vehicle {lstbox_params_choices[5]} Information"
    params_display_heading7 = f"Vehicle {lstbox_params_choices[6]} Information"
    params_display_heading8 = f"Vehicle {lstbox_params_choices[7]} Information"

    lstbox_params_dc_choices = ["plot", "array"]
    lstbox_params_ext_cond_choices = ["values"]

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        # Instance varibles
        self.var_lstbox_parameters_choices = tkinter.StringVar()
        self.var_lstbox_parameters_choices.set(self.lstbox_params_choices)
        self.var_lstbox_params_user_choice = tkinter.StringVar()

        self.var_lstbox_params_dc = tkinter.StringVar()
        self.var_lstbox_params_dc.set(self.lstbox_params_dc_choices)

        self.var_lstbox_params_ext_cond = tkinter.StringVar()
        self.var_lstbox_params_ext_cond.set(self.lstbox_params_ext_cond_choices)

        # Widgets
        self.create_widgets()

        # Bindings
        self.lstbox_params.bind('<<ListboxSelect>>', self.set_lstbox_params_user_choice)
        self.lstbox_dc_params.bind('<<ListboxSelect>>', self.set_lstbox_params_dc_user_choice)
        self.lstbox_ext_cond_params.bind('<<ListboxSelect>>', self.set_lstbox_params_ext_cond_user_choice)

        # Widget placements
        self.grid(row=1, column=0)

    def create_widgets(self):
        ttk.Label(self, text="Parameters", font=VehicleDynamicsApp.heading_style).grid(row=2, column=0,
                                                                                       sticky=tkinter.W, pady=(10, 0))
        self.create_vehicle_widgets()  # Parameter Widgets - Vehicle
        self.create_dc_widgets()  # Parameter Widgets - Drive Cycle
        self.create_ext_cond_widgets()  # Parameter Widgets - External Conditions

    def create_vehicle_widgets(self):
        ttk.Label(self, text="Vehicle", font=VehicleDynamicsApp.heading_style2).grid(row=3, column=0,
                                                                                     sticky=tkinter.W)
        self.lstbox_params = tkinter.Listbox(self, width=50, listvariable=self.var_lstbox_parameters_choices,
                                             selectmode="single", exportselection=False,
                                             height=len(self.lstbox_params_choices))
        self.lstbox_params.grid(row=4, column=0, rowspan=len(self.lstbox_params_choices))

    def create_dc_widgets(self):
        lbl_param_dc = ttk.Label(self, text="Drive Cycle", font=VehicleDynamicsApp.heading_style2)
        self.lstbox_dc_params = tkinter.Listbox(self, width=50, selectmode="single",
                                                listvariable=self.var_lstbox_params_dc,
                                                exportselection=False,
                                                height=len(self.lstbox_params_dc_choices))
        lbl_param_dc.grid(row=4 + len(self.lstbox_params_choices), column=0, sticky=tkinter.W)
        self.lstbox_dc_params.grid(row=4 + len(self.lstbox_params_choices) + 1, column=0)

    def create_ext_cond_widgets(self):
        lbl_param_ext_cond = ttk.Label(self, text="External Conditions", font=VehicleDynamicsApp.heading_style2)
        self.lstbox_ext_cond_params = tkinter.Listbox(self, width=50, selectmode="single",
                                                      listvariable=self.var_lstbox_params_ext_cond,
                                                      exportselection=False,
                                                      height=len(self.lstbox_params_ext_cond_choices))
        lbl_param_ext_cond.grid(row=4 + len(self.lstbox_params_choices) + 1 + len(self.lstbox_params_dc_choices),
                                column=0,
                                sticky="news")
        self.lstbox_ext_cond_params.grid(
            row=4 + len(self.lstbox_params_choices) + 1 + len(self.lstbox_params_dc_choices) + 1,
            column=0)

    def set_lstbox_params_user_choice(self, event) -> None:
        self.var_lstbox_params_user_choice.set(self.lstbox_params.get(self.lstbox_params.curselection()))
        user_choice = self.var_lstbox_params_user_choice.get()
        text = f'Vehicle {user_choice} Information'
        MainDisplay(parent_fme=self.parent.fme_display, text=text, sim_vars_instance=self.parent.sim_vars)

    def set_lstbox_params_dc_user_choice(self, event) -> None:
        user_selection = self.lstbox_dc_params.get(self.lstbox_dc_params.curselection())
        DCParameterDisplay(parent_fme=self.parent.fme_display, text=user_selection, sim_vars_instance=self.parent.sim_vars)

    def set_lstbox_params_ext_cond_user_choice(self, event) -> None:
        ExtCondParameterDisplay(parent_fme=self.parent.fme_display,
                                text='External Conditions Information',
                                sim_vars_instance= self.parent.sim_vars)


class ResultInput(ttk.Frame):
    lstbox_results_choices = ["Desired Acceleration", "Desired Accelerating Force", "Aerodynamic Force",
                              "Rolling Grade Force", "Demand Torque", "Max. Torque", "Limit Regeneration",
                              "Limit Torque", "Motor Torque", "Actual Accelerating Force", "Actual Acceleration",
                              "Motor Speed", "Actual Speed", "Distance", "Motor Demand Power", "Limit Power",
                              "Battery Demand", "Battery Current"]

    def __init__(self, parent, start_row_num) -> None:
        super().__init__(parent)

        # Instance variables
        self.parent = parent
        self.start_row_num = start_row_num
        self.error_msg = tkinter.StringVar()

        self.var_lstbox_results = tkinter.StringVar()
        self.var_lstbox_results.set(self.lstbox_results_choices)

        # Widgets
        ttk.Label(self, text="Results", font=VehicleDynamicsApp.heading_style).grid(row=0, column=0, sticky=tkinter.W)
        bttn_sim = ttk.Button(self, text="Simulate", command=self.simulate)

        # Widget grid placement
        bttn_sim.grid(row=start_row_num + 1, column=0, sticky=tkinter.W)
        self.grid(row=start_row_num, column=0, sticky=tkinter.W, pady=(10, 0))

    def simulate(self) -> None:
        try:
            self.parent.sim_vars.sim() # perform simulation and store it in sim_vars.sol
            self.lstbox_result = tkinter.Listbox(self, listvariable=self.var_lstbox_results, width=50,
                                                 selectmode="single", height=len(self.lstbox_results_choices),
                                                 exportselection=False) # Listbox created only after simulations

            # bindings
            self.lstbox_result.bind('<<ListboxSelect>>', self.cmd_lstbox_result)

            # Widget placements
            self.lstbox_result.grid(row=self.start_row_num + 2, column=0)
        except Exception as e:
            self.error_msg.set(e)
            ttk.Label(self, text=self.error_msg.get(), font=VehicleDynamicsApp.error_font_style, foreground='red',
                      width=40).grid(row=self.start_row_num + 2, column=0, sticky=tkinter.W)

    def cmd_lstbox_result(self, event) -> None:
        user_choice = self.lstbox_result.get(self.lstbox_result.curselection())
        ResultDisplay(parent_fme=self.parent.fme_display, text=user_choice, parent_obj=self, sim_vars_instance=self.parent.sim_vars)


class MainDisplay(ttk.Frame):
    """
    This class contains attributes and methods pertaining to Main Display (viewed on the right-hand side of the GUI
    window).
    """
    # Class variables
    dc_wildcard_txt = definations.ROOT_DIR + '\data\drive_cycles\*.txt'
    all_dc = [os.path.split(file_)[-1].split('.')[0] for file_ in glob.glob(dc_wildcard_txt)]  # all_dc lists all the

    # available drive cycles from drive_cycle database.

    def __init__(self, parent_fme: ttk.Frame, text: str, sim_vars_instance: InputSimVariables) -> None:
        super().__init__(parent_fme)

        if not isinstance(text, str):
            raise TypeError("Input text needs to be a string object.")

        if isinstance(sim_vars_instance, InputSimVariables):
            self.sim_vars_instance = sim_vars_instance
        else:
            raise TypeError("Parameter sim_vars_instance needs to be a InputSimVariables.")

        # Widgets - Basic Heading
        lbl = ttk.Label(self, text=text, font=VehicleDynamicsApp.heading_style)

        # Widgets - Based on Vehicle Parameters on the Input Frame
        if text == ParametersOnInputFrame.params_display_heading1:  # Basic Information
            self.create_basic_vehicle_params_display()
        elif text == ParametersOnInputFrame.params_display_heading2:  # Battery Cell Information
            self.create_battery_cell_params_display()
        elif text == ParametersOnInputFrame.params_display_heading3:  # Battery Module Information
            self.create_battery_module_params_display()
        elif text == ParametersOnInputFrame.params_display_heading4:  # Battery Pack Information
            self.create_battery_pack_params_display()
        elif text == ParametersOnInputFrame.params_display_heading5:  # Battery Motor Information
            self.create_motor_params_display()
        elif text == ParametersOnInputFrame.params_display_heading6:  # Battery Wheel Information
            self.create_wheel_params_display()
        elif text == ParametersOnInputFrame.params_display_heading7:  # Battery Drivetrain Information
            self.create_dt_params_display()
        elif text == ParametersOnInputFrame.params_display_heading8:  # Battery Design Information
            self.create_design_params_display()

        # Widget Placement
        lbl.grid(row=0, column=0, sticky=tkinter.W)
        self.grid(row=0, column=0, sticky="news")

    def create_basic_vehicle_params_display(self) -> None:
        """
        Creates a display for the vehicle's basic information.
        :return:
        """
        ttk.Label(self, text="Model").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Make").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Year").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Trim").grid(row=5, column=0, sticky=tkinter.W)

        # ttk.Label(self, text=self.parent_obj.ev_obj.model_name).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.sim_vars_instance.ev_obj_instances[0].model_name).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.sim_vars_instance.ev_obj_instances[0].manufacturer).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.sim_vars_instance.ev_obj_instances[0].year).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.sim_vars_instance.ev_obj_instances[0].trim).grid(row=5, column=1, sticky=tkinter.W)

    def create_battery_cell_params_display(self) -> None:
        """
        Widgets for the battery cell display.
        :return: None
        """
        ev_obj = self.sim_vars_instance.ev_obj_instances[0].pack
        ttk.Label(self, text="Manufacturer").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Chemistry").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Capacity [A hr]").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Mass [g]").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="V_max [V]").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="V_nom [V]").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="V_min [V]").grid(row=8, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Cell Energy, Wh").grid(row=9, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Cell Specific Energy, Wh/kg").grid(row=10, column=0, sticky=tkinter.W)

        ttk.Label(self, text=ev_obj.cell_manufacturer).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_chem).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_cap).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_mass).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_V_max).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_V_nom).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_V_min).grid(row=8, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_energy).grid(row=9, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.cell_spec_energy).grid(row=10, column=1, sticky=tkinter.W)

    def create_battery_module_params_display(self) -> None:
        """
        Creates a display for the vehicle's battery cell information.
        :return: None
        """
        ev_obj = self.sim_vars_instance.ev_obj_instances[0].pack
        ttk.Label(self, text="No. of parallel cells]").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="No. of series cells]").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="No. of tot. cells").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Overhead mass ratio").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Capacity [Ah]").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Mass [kg]").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Energy [kWh]").grid(row=8, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Specific Energy [Wh/kg]").grid(row=9, column=0, sticky=tkinter.W)

        ttk.Label(self, text=ev_obj.Np).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.Ns).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.total_no_cells).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.module_overhead_mass).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.module_cap).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.module_mass).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.module_energy).grid(row=8, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.module_specific_energy).grid(row=9, column=1, sticky=tkinter.W)

    def create_battery_pack_params_display(self) -> None:
        """
        Widgets for the battery pack display.
        :return:
        """
        ev_obj = self.sim_vars_instance.ev_obj_instances[0].pack
        ttk.Label(self, text="Tot. Modules").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Mass, kg").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Energy, Wh").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Specific Energy, Wh/kg").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Minimum Potential, V").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Nominal Potential, V").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Maximum Potential, V").grid(row=8, column=0, sticky=tkinter.W)

        ttk.Label(self, text=ev_obj.num_modules).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.pack_mass).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.pack_energy).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.pack_energy).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.pack_V_min).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.pack_V_nom).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=ev_obj.pack_V_max).grid(row=8, column=1, sticky=tkinter.W)

    def create_motor_params_display(self) -> None:
        """
        Widgets for the motor display.
        :return: None
        """
        motor_info = self.sim_vars_instance.ev_obj_instances[0].motor
        ttk.Label(self, text="Motor Type").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Rated Speed, RPM").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Max. Speed, RPM").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Max. Torque, Nm").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Efficiency").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Inertia, kg m^2").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Max. Power, kW").grid(row=8, column=0, sticky=tkinter.W)

        ttk.Label(self, text=motor_info.motor_type).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=motor_info.RPM_r).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=motor_info.RPM_max).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=motor_info.L_max).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=motor_info.eff).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=motor_info.I).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=motor_info.P_max).grid(row=8, column=1, sticky=tkinter.W)

    def create_wheel_params_display(self) -> None:
        wheel_info = self.sim_vars_instance.ev_obj_instances[0].drive_train.wheel

        ttk.Label(self, text="Radius, m").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Inertia, kg m^2").grid(row=3, column=0, sticky=tkinter.W)

        ttk.Label(self, text= wheel_info.r).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text= wheel_info.I).grid(row=3, column=1, sticky=tkinter.W)

    def create_dt_params_display(self) -> None:
        dt_info = self.sim_vars_instance.ev_obj_instances[0].drive_train
        ttk.Label(self, text="Gearbox Ratio").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Inertia, kg m^2").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="No. wheels").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="inverter Efficiency").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Fraction of regeneration").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Efficiency").grid(row=7, column=0, sticky=tkinter.W)

        ttk.Label(self, text=dt_info.gear_box.N).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=dt_info.gear_box.I).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=dt_info.num_wheel).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=dt_info.inverter_eff).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=dt_info.frac_regen_torque).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=dt_info.eff).grid(row=7, column=1, sticky=tkinter.W)

    def create_design_params_display(self) -> None:
        design_info = self.sim_vars_instance.ev_obj_instances[0]
        ttk.Label(self, text="Drag Coefficient").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Frontal Area, m^2").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Mass [kg]").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Payload Cap [kg]").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Curb Mass [kg]").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Rotational Mass [kg]").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Maximum Speed [km/h]").grid(row=8, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Overhead Power [W]").grid(row=9, column=0, sticky=tkinter.W)

        ttk.Label(self, text=design_info.C_d).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.A_front).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.m).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.payload_capacity).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.curb_mass).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.rot_mass).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.max_speed).grid(row=8, column=1, sticky=tkinter.W)
        ttk.Label(self, text=design_info.overhead_power).grid(row=9, column=1, sticky=tkinter.W)


class InputsDisplay(MainDisplay):
    """
    Attributes and methods for the contents on the Display Frame corresponding to the Inputs selected on the Input
    Frame.
    """
    def __init__(self, parent_fme, text: str, sim_vars_instance: InputSimVariables) -> \
            None:
        super().__init__(parent_fme=parent_fme, text=text, sim_vars_instance=sim_vars_instance)

        # Instance variables
        self.var_rho = tkinter.StringVar()
        self.var_road_grade = tkinter.StringVar()
        self.var_road_force = tkinter.StringVar()

        self.create_widgets(text=text)

    def create_widgets(self, text) -> None:
        if text == InputsOnInputFrame.input_display_heading1:  # EV input
            self.create_EV_widgets()
        elif text == InputsOnInputFrame.input_display_heading2:  # Drive Cycle input
            self.create_DC_widgets()
        elif text == InputsOnInputFrame.input_display_heading3:  # External Conditions
            self.create_ExtCond_widgets()

    def create_EV_widgets(self) -> None:
        row_num = 2
        ttk.Label(self, text="EV Alias").grid(row=row_num, column=0)
        self.combobox_EV_alias = ttk.Combobox(self, height=10)
        self.combobox_EV_alias['values'] = EV_sim.EVFromDatabase.list_all_EV_alias(
            file_dir=VehicleDynamicsApp.EV_DATABASE_DIR)

        # Bindings
        self.combobox_EV_alias.bind('<<ComboboxSelected>>', self.combobox_EV_alias_select)

        # Widget placement
        self.combobox_EV_alias.grid(row=row_num, column=1)

    def create_DC_widgets(self) -> None:
        row_num = 2
        ttk.Label(self, text="Drive Cycle").grid(row=row_num, column=0, sticky=tkinter.W)
        self.combobox_dc = ttk.Combobox(self, height=10)
        self.combobox_dc['values'] = self.all_dc

        self.combobox_dc.bind('<<ComboboxSelected>>', self.combobox_dc_select)

        # Widget - Plot
        self.tk_canvas_dc_plot = tkinter.Canvas(self)
        fig_dc_plot = plt.figure()
        self.ax_dc_plot = fig_dc_plot.add_subplot()
        self.ax_dc_plot.set_xlabel('Time [s]')
        self.ax_dc_plot.set_ylabel('Speed [km/h]')
        self.cavas_dc_plot = FigureCanvasTkAgg(figure=fig_dc_plot, master=self.tk_canvas_dc_plot)

        # Widget placement
        self.combobox_dc.grid(row=row_num, column=1)
        self.tk_canvas_dc_plot.grid(row=row_num + 1, column=0, columnspan=2, pady=10)
        self.cavas_dc_plot.get_tk_widget().pack()

        plt.close()

    def create_ExtCond_widgets(self) -> None:
        def update_rho(event):
            if self.var_rho.get():
                self.sim_vars_instance.update_rho(float(self.var_rho.get()))

        def update_grade(event):
            if self.var_road_grade.get():
                self.sim_vars_instance.ext_cond_obj.road_grade = float(self.var_road_grade.get())

        def update_force(event):
            if self.var_road_force.get():
                self.sim_vars_instance.ext_cond_obj.road_force = float(self.var_road_force.get())

        ttk.Label(self, text="Air Density, kg/m^3").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Grade, %").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Force, N").grid(row=4, column=0, sticky=tkinter.W)

        entry_rho = ttk.Entry(self, textvariable=self.var_rho)
        entry_grade = ttk.Entry(self, textvariable=self.var_road_grade)
        entry_force = ttk.Entry(self, textvariable=self.var_road_force)

        # binds
        entry_rho.bind('<KeyRelease>', update_rho)
        entry_grade.bind('<KeyRelease>', update_grade)
        entry_force.bind('<KeyRelease>', update_force)

        # Widget grid placements
        entry_rho.grid(row=2, column=1)
        entry_grade.grid(row=3, column=1)
        entry_force.grid(row=4, column=1)


    def combobox_EV_alias_select(self, event) -> None:
        alias_name = self.combobox_EV_alias.get()
        self.sim_vars_instance.update_EV_instance(instance_index=0, alias_name=alias_name)

    def combobox_dc_select(self, event) -> None:
        # self.parent_obj.dc_obj = EV_sim.DriveCycle(self.combobox_dc.get(),
        #                                            folder_dir=VehicleDynamicsApp.DRIVECYCLE_FOLDER_DIR)
        drive_cycle_name = self.combobox_dc.get()
        self.sim_vars_instance.update_drivecycle_instance(drive_cycle_name=drive_cycle_name)
        # plot on the canvas
        self.ax_dc_plot.clear()
        self.ax_dc_plot.plot(self.sim_vars_instance.dc_obj.t, self.sim_vars_instance.dc_obj.speed_kmph)
        self.ax_dc_plot.set_xlabel('Time [s]')
        self.ax_dc_plot.set_ylabel('Speed [km/h]')
        self.cavas_dc_plot.draw()


class DCParameterDisplay(MainDisplay):
    """
    Contains attributes and methods for the display for the drive cycle. A plot or array for the drive cycle can
    be viewed.
    """
    MAX_ARRAY_LENGTH = 20

    def __init__(self, parent_fme, text: str, sim_vars_instance: InputSimVariables):
        super().__init__(parent_fme=parent_fme, text=text, sim_vars_instance=sim_vars_instance)

        # If drive cycle is not set, then attempts to plot or list arrays will result in Attribute exception.
        try:
            if text == ParametersOnInputFrame.lstbox_params_dc_choices[0]:  # plot
                self.create_plot_display()
            elif text == ParametersOnInputFrame.lstbox_params_dc_choices[1]:  # array
                self.create_array_display()
        except AttributeError:
            ttk.Label(self, text="Set Drive Cycle in the Inputs section.", font=VehicleDynamicsApp.error_font_style,
                      foreground="red").grid(row=0, column=0)

        # # Widget grid placement
        # self.grid(row=0, column=0, sticky="news")

    def create_plot_display(self):
        tk_canvas = tkinter.Canvas(self)
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(figure=fig, master=tk_canvas)
        ax = fig.add_subplot()
        ax.plot(self.sim_vars_instance.dc_obj.t, self.sim_vars_instance.dc_obj.speed_kmph)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Speed [km/h]')

        # widget placement
        tk_canvas.grid(row=0, column=0, sticky="news")
        canvas.get_tk_widget().grid(row=0, column=0)

        plt.close()

    def create_array_display(self):
        error_msg = tkinter.StringVar()

        if len(self.sim_vars_instance.dc_obj.t) > self.MAX_ARRAY_LENGTH:
            max_length = self.MAX_ARRAY_LENGTH
            error_msg.set("Array too long. Results have been appended")
        else:
            max_length = len(self.sim_vars_instance.dc_obj.t)

        ttk.Label(self, text="Time [s]").grid(row=0, column=0)
        ttk.Label(self, text="Speed [km/h]").grid(row=0, column=2)

        for row_i in range(0, max_length):
            ttk.Label(self, text=self.sim_vars_instance.dc_obj.t[row_i]).grid(row=row_i + 1, column=0)
            ttk.Label(self, text=self.sim_vars_instance.dc_obj.speed_kmph[row_i]).grid(row=row_i + 1, column=2)

        ttk.Label(self, text=error_msg.get()).grid(row=self.MAX_ARRAY_LENGTH + 5, column=0)


class ExtCondParameterDisplay(MainDisplay):
    def __init__(self, parent_fme: ttk.Frame, text: str, sim_vars_instance: InputSimVariables):
        super().__init__(parent_fme=parent_fme, text=text, sim_vars_instance=sim_vars_instance)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Air Density, kg/m^3").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Grade, %").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Force, N").grid(row=4, column=0, sticky=tkinter.W)

        ttk.Label(self, text=self.sim_vars_instance.ext_cond_obj.rho).grid(row=2, column=1, sticky=tkinter.W, padx=10)
        ttk.Label(self, text=self.sim_vars_instance.ext_cond_obj.road_grade).grid(row=3, column=1, sticky=tkinter.W, padx=10)
        ttk.Label(self, text=self.sim_vars_instance.ext_cond_obj.road_force).grid(row=4, column=1, sticky=tkinter.W, padx=10)

        # # variables
        # self.error_msg = tkinter.StringVar()
        #
        # # Check for incomplete external conditions
        # try:
        #     float(air_density)
        # except:
        #     self.error_msg.set("Invalid Air Density. Indicate Air Density in the Inputs Section.")
        #
        # try:
        #     float(road_grade)
        # except:
        #     self.error_msg.set("Invalid road grade. Indicate road grade in the Inputs Section.")
        #
        # try:
        #     float(road_force)
        # except:
        #     self.error_msg.set("Invalid road force. Indicate road force in the Inputs Section.")

        # # Widgets
        # ttk.Label(self, text="Air Density, kg/m^3").grid(row=2, column=0, sticky=tkinter.W)
        # ttk.Label(self, text="Road Grade, %").grid(row=3, column=0, sticky=tkinter.W)
        # ttk.Label(self, text="Road Force, N").grid(row=4, column=0, sticky=tkinter.W)
        #
        # ttk.Label(self, text=air_density).grid(row=2, column=1, sticky=tkinter.W, padx=10)
        # ttk.Label(self, text=road_grade).grid(row=3, column=1, sticky=tkinter.W, padx=10)
        # ttk.Label(self, text=road_force).grid(row=4, column=1, sticky=tkinter.W, padx=10)
        #
        # ttk.Label(self, text=self.error_msg.get(), foreground='red', font=VehicleDynamicsApp.error_font_style) \
        #     .grid(row=5, column=0, columnspan=5)
        #
        # # Widget placement
        # self.grid(row=0, column=0, sticky="news")


class ResultDisplay(MainDisplay):
    """
    ResultDisplay contains attributes and methods pertaining to the display corresponding to the results section in the
    Input display. This section is activated after the simulation is performed.
    """

    # TODO: have the option of saving data and plots.
    def __init__(self, parent_fme, text: str, parent_obj: tkinter.Frame, sim_vars_instance: InputSimVariables) -> None:
        super().__init__(parent_fme=parent_fme, text=text, sim_vars_instance=sim_vars_instance)

        # # Check for the inputs, particularly parent_obj needs to be a ResultInput Object.
        # if not isinstance(self.parent_obj, ResultInput):
        #     raise TypeError("parent_obj needs to be a ResultInput object.")
        # # Furthermore, the parent_obj needs to have a simulation solution object.
        # if not isinstance(self.parent_obj.sol, EV_sim.sol.Solution):
        #     raise TypeError("Solution object not found inside the parent_obj")

        # Widgets
        self.create_widgets(text=text)

    def create_widgets(self, text: str) -> None:
        """
        Creates the widgets on the Display. The content of the Display changes depending on the user selection.
        :param text: class input text
        :return: None
        """
        x_label = 'Time [min]'
        sol_obj = self.sim_vars_instance.sol
        x_values = sol_obj.t

        if text == ResultInput.lstbox_results_choices[0]:
            self.create_plot(x_values=x_values, y_values=sol_obj.des_acc,
                             x_label=x_label, y_label=r'Desired Acceleration [m/$s^2$]')
        elif text == ResultInput.lstbox_results_choices[1]:
            self.create_plot(x_values=x_values, y_values=sol_obj.des_acc_F,
                             x_label=x_label, y_label='Desired Acceleration Force [N]')
        elif text == ResultInput.lstbox_results_choices[2]:
            self.create_plot(x_values=x_values, y_values=sol_obj.aero_F,
                             x_label=x_label, y_label='Aerodynamic Force [N]')
        elif text == ResultInput.lstbox_results_choices[3]:
            self.create_plot(x_values=x_values, y_values=sol_obj.roll_grade_F,
                             x_label=x_label, y_label='Rolling Grade Force [N]')
        elif text == ResultInput.lstbox_results_choices[4]:
            self.create_plot(x_values=x_values, y_values=sol_obj.demand_torque,
                             x_label=x_label, y_label='Demand Torque [Nm]')
        elif text == ResultInput.lstbox_results_choices[5]:
            self.create_plot(x_values=x_values, y_values=sol_obj.max_torque,
                             x_label=x_label, y_label='Max. Torque [Nm]')
        elif text == ResultInput.lstbox_results_choices[6]:
            self.create_plot(x_values=x_values, y_values=sol_obj.limit_regen,
                             x_label=x_label, y_label='Limit Regeneration [Nm]')
        elif text == ResultInput.lstbox_results_choices[7]:
            self.create_plot(x_values=x_values, y_values=sol_obj.limit_torque,
                             x_label=x_label, y_label='Limit Torque [Nm]')
        elif text == ResultInput.lstbox_results_choices[8]:
            self.create_plot(x_values=x_values, y_values=sol_obj.motor_torque,
                             x_label=x_label, y_label='Motor Torque [Nm]')
        elif text == ResultInput.lstbox_results_choices[9]:
            self.create_plot(x_values=x_values, y_values=sol_obj.actual_acc_F,
                             x_label=x_label, y_label='Actual Acceleration Force [N]')
        elif text == ResultInput.lstbox_results_choices[10]:
            self.create_plot(x_values=x_values, y_values=sol_obj.actual_acc,
                             x_label=x_label, y_label=r'Actual Acceleration $[m/s^2]$')
        elif text == ResultInput.lstbox_results_choices[11]:
            self.create_plot(x_values=x_values, y_values=sol_obj.motor_speed,
                             x_label=x_label, y_label='Motor Speed [RPM]')
        elif text == ResultInput.lstbox_results_choices[12]:
            self.create_plot(x_values=x_values, y_values=sol_obj.actual_speed_kmph,
                             x_label=x_label, y_label='Actual Speed [km/h]')
        elif text == ResultInput.lstbox_results_choices[13]:
            self.create_plot(x_values=x_values, y_values=sol_obj.actual_speed_kmph,
                             x_label=x_label, y_label='Distance [km]')
        elif text == ResultInput.lstbox_results_choices[14]:
            self.create_plot(x_values=x_values, y_values=sol_obj.demand_power,
                             x_label=x_label, y_label='Motor Demand Power [kW]')
        elif text == ResultInput.lstbox_results_choices[15]:
            self.create_plot(x_values=x_values, y_values=sol_obj.limit_power,
                             x_label=x_label, y_label='Limit Power [kW]')
        elif text == ResultInput.lstbox_results_choices[16]:
            self.create_plot(x_values=x_values, y_values=sol_obj.battery_demand,
                             x_label=x_label, y_label='Battery power demand [kW]')
        elif text == ResultInput.lstbox_results_choices[17]:
            self.create_plot(x_values=x_values, y_values=sol_obj.current,
                             x_label=x_label, y_label='Battery Pack Current [A]')

    def create_plot_canvas(self) -> None:
        tk_canvas = tkinter.Canvas(self)
        fig = plt.figure()
        self.ax = fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(figure=fig, master=tk_canvas)

        # Widget grid placement
        tk_canvas.grid(row=1, column=0)
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def create_plot(self, x_values, y_values, x_label, y_label) -> None:
        """
        Creates the time vs. battery power demand plot on the Display.
        :param x_values: (np.ndarray) x_values for the plot
        :param y_values: (np.ndarray) y_values for the plot.
        :return: None
        """
        self.create_plot_canvas()
        self.ax.clear()
        self.ax.plot(x_values, y_values)
        self.ax.set_xlabel(xlabel=x_label)
        self.ax.set_ylabel(ylabel=y_label)
        self.canvas.draw()
        plt.close()


if __name__ == '__main__':
    VehicleDynamicsApp()
