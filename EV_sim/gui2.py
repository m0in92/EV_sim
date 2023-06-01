import glob
import os
import tkinter
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import EV_sim
from EV_sim.config import definations


class VehicleDynamicsApp2(tkinter.Tk):
    heading_style = ('Helvetica', 10, 'bold')
    heading_style2 = ('Helvetica', 8, 'bold')
    error_font_style = ('Helvetica', 10, 'bold')

    EV_DATABASE_DIR = definations.ROOT_DIR + "/data/EV/EV_dataset.csv"
    DRIVECYCLE_FOLDER_DIR = definations.ROOT_DIR + "/data/drive_cycles/"

    def __init__(self):
        # root/window
        super().__init__()
        self.title()
        self.title('EV Simulator')
        self.iconbitmap(definations.ROOT_DIR + '/icon.ico')
        self.geometry('1200x800')

        # instance variables
        self.var_lstbox_inputs_user_choice = tkinter.StringVar()
        self.set_two_decimal = tkinter.BooleanVar() # option whether to show results in two decimal places.
        self.set_two_decimal.set(False) # Initialize so that this option is False

        # Style, only for the paned window scroll
        style = ttk.Style()
        style.theme_use('classic')

        # Widgets - Menubar and PanedWindow
        self.mb = tkinter.Menu(self)
        option_menu = tkinter.Menu(self.mb)
        option_menu.add_command(label="Show to two decimal", command=self.show_two_decimal_cmd)
        self.mb.add_cascade(label="Options", menu=option_menu)

        self.pw = ttk.PanedWindow(self, orient=tkinter.HORIZONTAL)

        # Widget - Input and Display Frames
        self.InputFrame = InputAndDisplayFrames(parent=self.pw)

        # Widget grid placements
        self.pw.grid(row=0, column=0, sticky="news")

        # Row and column configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(menu=self.mb)

        # main loop
        self.mainloop()

    def show_two_decimal_cmd(self):
        self.set_two_decimal.set(True)


class InputAndDisplayFrames(ttk.Frame):
    # Class variables
    lstbox_inputs_choices = ["EV", "Drive Cycle", "External Conditions"] # all main choices in the input section
    lstbox_params_choices = ["Basic", "Cell", "Module", "Pack", "Motor", "Wheel", "Drivetrain", "Design"]
    lstbox_params_dc_choices = ["plot", "array"]
    lstbox_params_ext_cond_choices = ["values"]

    input_display_heading1 = f"{lstbox_inputs_choices[0]}"
    input_display_heading2 = f"{lstbox_inputs_choices[1]}"
    input_display_heading3 = f"{lstbox_inputs_choices[2]}"

    params_display_heading1 = f"Vehicle {lstbox_params_choices[0]} Information"
    params_display_heading2 = f"Vehicle {lstbox_params_choices[1]} Information"
    params_display_heading3 = f"Vehicle {lstbox_params_choices[2]} Information"
    params_display_heading4 = f"Vehicle {lstbox_params_choices[3]} Information"
    params_display_heading5 = f"Vehicle {lstbox_params_choices[4]} Information"
    params_display_heading6 = f"Vehicle {lstbox_params_choices[5]} Information"
    params_display_heading7 = f"Vehicle {lstbox_params_choices[6]} Information"
    params_display_heading8 = f"Vehicle {lstbox_params_choices[7]} Information"

    def __init__(self, parent) -> None:
        super().__init__(parent)

        # Instance variables
        self.var_lstbox_inputs_choices = tkinter.StringVar()
        self.var_lstbox_inputs_choices.set(InputAndDisplayFrames.lstbox_inputs_choices)
        self.var_lstbox_inputs_user_choice = tkinter.StringVar()

        self.var_lstbox_parameters_choices = tkinter.StringVar()
        self.var_lstbox_parameters_choices.set(InputAndDisplayFrames.lstbox_params_choices)
        self.var_lstbox_params_user_choice = tkinter.StringVar()

        self.var_lstbox_params_dc = tkinter.StringVar()
        self.var_lstbox_params_dc.set(self.lstbox_params_dc_choices)

        self.var_lstbox_params_ext_cond = tkinter.StringVar()
        self.var_lstbox_params_ext_cond.set(self.lstbox_params_ext_cond_choices)

        self.ev_obj = EV_sim.EV("Volt_2017") # stores the EV object, initialized with a random EV
        self.dc_obj = EV_sim.DriveCycle(MainDisplay.all_dc[0], folder_dir=VehicleDynamicsApp2.DRIVECYCLE_FOLDER_DIR)
        # stores the DriveCycle object and initializes with a the first drive cycle text file in the
        # data/drive_cycles folder
        self.var_air_pressure = tkinter.StringVar()
        self.var_road_grade = tkinter.StringVar()
        self.var_road_force = tkinter.StringVar()

        # Inputs Widgets
        ttk.Label(self, text="Inputs", font=VehicleDynamicsApp2.heading_style).grid(row=0, column=0, sticky="news")
        self.lstbox_inputs = tkinter.Listbox(self, width=50, listvariable= self.var_lstbox_inputs_choices,
                                             selectmode="single", exportselection=False,
                                             height=len(self.lstbox_inputs_choices))

        # Display Widgets
        self.fme_display = ttk.Label(parent)

        # Parameter Widgets - Vehicle
        ttk.Label(self, text="Parameters", font=VehicleDynamicsApp2.heading_style).grid(row=2, column=0,
                                                                                        sticky=tkinter.W, pady=(10,0))
        ttk.Label(self, text="Vehicle", font=VehicleDynamicsApp2.heading_style2).grid(row=3, column=0,
                                                                                      sticky= tkinter.W)
        self.lstbox_params = tkinter.Listbox(self, width=50, listvariable=self.var_lstbox_parameters_choices,
                                             selectmode="single", exportselection=False,
                                             height=len(self.lstbox_params_choices))

        # Parameter Widgets - Drive Cycle
        lbl_param_dc = ttk.Label(self, text="Drive Cycle", font=VehicleDynamicsApp2.heading_style2)
        self.lstbox_dc_params = tkinter.Listbox(self, width=50, selectmode="single",
                                                listvariable=self.var_lstbox_params_dc,
                                                exportselection=False,
                                                height=len(self.lstbox_params_dc_choices))

        # Parameter Widgets - External Conditions
        lbl_param_ext_cond = ttk.Label(self, text="External Conditions", font=VehicleDynamicsApp2.heading_style2)
        self.lstbox_ext_cond_params = tkinter.Listbox(self, width=50, selectmode="single",
                                                      listvariable=self.var_lstbox_params_ext_cond,
                                                      exportselection=False,
                                                      height=len(self.lstbox_params_ext_cond_choices))

        # Results Widget
        ResultInput(parent=self,
                      start_row_num=4 + len(self.lstbox_params_choices) + 1 + len(self.lstbox_params_dc_choices)+2)

        # Bindings
        self.lstbox_inputs.bind('<<ListboxSelect>>', self.set_lstbox_input_user_choice)
        self.lstbox_params.bind('<<ListboxSelect>>', self.set_lstbox_params_user_choice)
        self.lstbox_dc_params.bind('<<ListboxSelect>>', self.set_lstbox_params_dc_user_choice)
        self.lstbox_ext_cond_params.bind('<<ListboxSelect>>', self.set_lstbox_params_ext_cond_user_choice)

        # Widget placement
        self.lstbox_inputs.grid(row=1, column=0, sticky="news")
        self.grid(row=0, column=0)
        parent.add(self)
        self.fme_display.grid(row=0, column=1, sticky="news")
        self.lstbox_params.grid(row=4, column=0, rowspan=len(self.lstbox_params_choices))
        lbl_param_dc.grid(row=4+len(self.lstbox_params_choices), column=0, sticky=tkinter.W)
        self.lstbox_dc_params.grid(row=4+len(self.lstbox_params_choices)+1, column=0)
        lbl_param_ext_cond.grid(row=4+len(self.lstbox_params_choices)+1+len(self.lstbox_params_dc_choices), column=0,
                                sticky="news")
        self.lstbox_ext_cond_params.grid(row=4+len(self.lstbox_params_choices)+1+len(self.lstbox_params_dc_choices)+1,
                                         column=0)
        parent.add(self.fme_display)

    def set_lstbox_input_user_choice(self, event) -> None:
        self.var_lstbox_inputs_user_choice.set(self.lstbox_inputs.get(self.lstbox_inputs.curselection()))
        if self.var_lstbox_inputs_user_choice.get() == self.input_display_heading1:
            MainDisplay(self.fme_display, text=self.input_display_heading1, parent_obj=self)
        elif self.var_lstbox_inputs_user_choice.get() == self.input_display_heading2:
            MainDisplay(self.fme_display, text=self.input_display_heading2, parent_obj=self)
        elif self.var_lstbox_inputs_user_choice.get() == self.input_display_heading3:
            MainDisplay(self.fme_display, text=self.input_display_heading3, parent_obj=self)

    def set_lstbox_params_user_choice(self, event) -> None:
        self.var_lstbox_params_user_choice.set(self.lstbox_params.get(self.lstbox_params.curselection()))
        user_choice = self.var_lstbox_params_user_choice.get()
        if user_choice == self.lstbox_params_choices[0]: # Basic parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading1, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[1]: # Battery cell parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading2, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[2]: # Battery module parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading3, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[3]: # Battery module parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading4, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[4]: # Battery module parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading5, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[5]: # Battery module parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading6, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[6]: # Battery module parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading7, parent_obj=self)
        elif user_choice == self.lstbox_params_choices[7]: # Battery module parameter
            MainDisplay(parent_fme=self.fme_display, text=self.params_display_heading8, parent_obj=self)

    def set_lstbox_params_dc_user_choice(self, event) -> None:
        user_selection = self.lstbox_dc_params.get(self.lstbox_dc_params.curselection())
        DCParameterDisplay(parent=self.fme_display, user_selection=user_selection, dc_obj=self.dc_obj)

    def set_lstbox_params_ext_cond_user_choice(self, event) -> None:
        ExtCondParameterDisplay(parent=self.fme_display, air_density=self.var_air_pressure.get(),
                                road_grade=self.var_road_grade.get(), road_force=self.var_road_force.get())


class MainDisplay(ttk.Frame):
    # Class variables
    dc_wildcard_txt = definations.ROOT_DIR + '\data\drive_cycles\*.txt'
    all_dc = [os.path.split(file_)[-1].split('.')[0] for file_ in glob.glob(dc_wildcard_txt)]  # all_dc lists all the
    # available drive cycles from drive_cycle database.

    def __init__(self, parent_fme, text: str, parent_obj: tkinter.Frame) -> None:
        super().__init__(parent_fme)
        self.parent_obj = parent_obj

        if isinstance(parent_obj.ev_obj, EV_sim.EV):
            self.ev_obj = parent_obj.ev_obj
        else:
            raise TypeError("Cannot find EV instance inside parent_obj.")

        if isinstance(parent_obj.dc_obj, EV_sim.DriveCycle):
            self.dc_obj = parent_obj.dc_obj
        else:
            raise TypeError("Cannot find DriveCycle instance inside parent_obj.")

        # Widgets - Basic Heading
        lbl = ttk.Label(self, text=text, font=VehicleDynamicsApp2.heading_style)

        # Widgets - Based on Inputs on the Input Frame
        if text == InputAndDisplayFrames.input_display_heading1: # EV input
            self.create_EV_widgets()
        elif text == InputAndDisplayFrames.input_display_heading2: # Drive Cycle input
            self.create_DC_widgets()
        elif text == InputAndDisplayFrames.input_display_heading3: # External Conditions
            self.create_ExtCond_widgets()

        # Widgets - Based on Vehicle Parameters on the Input Frame
        if text == InputAndDisplayFrames.params_display_heading1: # Basic Information
            self.create_basic_vehicle_params_display()
        elif text == InputAndDisplayFrames.params_display_heading2: # Battery Cell Information
            self.create_battery_cell_params_display()
        elif text == InputAndDisplayFrames.params_display_heading3: # Battery Module Information
            self.create_battery_module_params_display()
        elif text == InputAndDisplayFrames.params_display_heading4: # Battery Pack Information
            self.create_battery_pack_params_display()
        elif text == InputAndDisplayFrames.params_display_heading5: # Battery Motor Information
            self.create_battery_motor_params_display()
        elif text == InputAndDisplayFrames.params_display_heading6: # Battery Wheel Information
            self.create_battery_wheel_params_display()
        elif text == InputAndDisplayFrames.params_display_heading7: # Battery Drivetrain Information
            self.create_battery_dt_params_display()
        elif text == InputAndDisplayFrames.params_display_heading8: # Battery Design Information
            self.create_battery_design_params_display()

        # Widgets - Based on Results on the Input Frame
        if text == ResultInput.lstbox_results_choices[0]:
            self.create_power_demand_plot()

        # Widget Placement
        lbl.grid(row=0, column=0, sticky= tkinter.W)
        self.grid(row=0, column=0, sticky="news")

    def create_EV_widgets(self) -> None:
        row_num = 2
        ttk.Label(self, text="EV Alias").grid(row=row_num, column=0)
        self.combobox_EV_alias = ttk.Combobox(self, height=10)
        self.combobox_EV_alias['values'] = EV_sim.EV.list_all_EV_alias(file_dir=VehicleDynamicsApp2.EV_DATABASE_DIR)

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
        self.tk_canvas_dc_plot.grid(row=row_num+1, column=0, columnspan=2, pady=10)
        self.cavas_dc_plot.get_tk_widget().pack()

    def create_ExtCond_widgets(self) -> None:
        ttk.Label(self, text="Air Density, kg/m^3").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Grade, %").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Force, N").grid(row=4, column=0, sticky=tkinter.W)

        ttk.Entry(self, textvariable=self.parent_obj.var_air_pressure).grid(row=2, column=1)
        ttk.Entry(self, textvariable=self.parent_obj.var_road_grade).grid(row=3, column=1)
        ttk.Entry(self, textvariable=self.parent_obj.var_road_force).grid(row=4, column=1)

    def combobox_EV_alias_select(self, event) -> None:
        self.parent_obj.ev_obj = EV_sim.EV(self.combobox_EV_alias.get())

    def combobox_dc_select(self, event) -> None:
        self.parent_obj.dc_obj = EV_sim.DriveCycle(self.combobox_dc.get(),
                                                   folder_dir=VehicleDynamicsApp2.DRIVECYCLE_FOLDER_DIR)
        # plot on the canvas
        self.ax_dc_plot.clear()
        self.ax_dc_plot.plot(self.parent_obj.dc_obj.t, self.parent_obj.dc_obj.speed_kmph)
        self.ax_dc_plot.set_xlabel('Time [s]')
        self.ax_dc_plot.set_ylabel('Speed [km/h]')
        self.cavas_dc_plot.draw()

    def create_basic_vehicle_params_display(self) -> None:
        """
        Creates a display for the vehicle's basic information.
        :return:
        """
        ttk.Label(self, text="Model").grid(row=2, column=0, sticky= tkinter.W)
        ttk.Label(self, text="Make").grid(row=3, column=0, sticky= tkinter.W)
        ttk.Label(self, text="Year").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Trim").grid(row=5, column=0, sticky= tkinter.W)

        ttk.Label(self, text=self.parent_obj.ev_obj.model_name).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.parent_obj.ev_obj.manufacturer).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.parent_obj.ev_obj.year).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.parent_obj.ev_obj.trim).grid(row=5, column=1, sticky=tkinter.W)

    def create_battery_cell_params_display(self) -> None:
        """
        Creates a display for the vehicle's battery cell information.
        :return: None
        """
        ev_obj = self.parent_obj.ev_obj.pack
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
        ev_obj = self.ev_obj.pack
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
        ttk.Label(self, text="Tot. Modules").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Mass, kg").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Energy, Wh").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Specific Energy, Wh/kg").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Minimum Potential, V").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Nominal Potential, V").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Maximum Potential, V").grid(row=8, column=0, sticky=tkinter.W)

        ttk.Label(self, text=self.ev_obj.pack.num_modules).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.pack.pack_mass).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.pack.pack_energy).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.pack.pack_energy).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.pack.pack_V_min).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.pack.pack_V_nom).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.pack.pack_V_max).grid(row=8, column=1, sticky=tkinter.W)

    def create_battery_motor_params_display(self) -> None:
        ttk.Label(self, text="Motor Type").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Rated Speed, RPM").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Max. Speed, RPM").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Max. Torque, Nm").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Efficiency").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Inertia, kg m^2").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Max. Power, kW").grid(row=8, column=0, sticky=tkinter.W)

        ttk.Label(self, text=self.ev_obj.motor.motor_type).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.motor.RPM_r).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.motor.RPM_max).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.motor.L_max).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.motor.eff).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.motor.I).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.motor.P_max).grid(row=8, column=1, sticky=tkinter.W)

    def create_battery_wheel_params_display(self) -> None:
        ttk.Label(self, text="Radius, m").grid(row=2, column=0, sticky= tkinter.W)
        ttk.Label(self, text="Inertia, kg m^2").grid(row=3, column=0, sticky= tkinter.W)

        ttk.Label(self, text=self.ev_obj.drive_train.wheel.r).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.drive_train.wheel.I).grid(row=3, column=1, sticky=tkinter.W)

    def create_battery_dt_params_display(self) -> None:
        ttk.Label(self, text="Gearbox Ratio").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Inertia, kg m^2").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="No. wheels").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="inverter Efficiency").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Fraction of regeneration").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Efficiency").grid(row=7, column=0, sticky=tkinter.W)

        ttk.Label(self, text=self.ev_obj.drive_train.gear_box.N).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.drive_train.gear_box.I).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.drive_train.num_wheel).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.drive_train.inverter_eff).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.drive_train.frac_regen_torque).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.drive_train.eff).grid(row=7, column=1, sticky=tkinter.W)

    def create_battery_design_params_display(self) -> None:
        ttk.Label(self, text="Drag Coefficient").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Frontal Area, m^2").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Mass [kg]").grid(row=4, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Payload Cap [kg]").grid(row=5, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Curb Mass [kg]").grid(row=6, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Rotational Mass [kg]").grid(row=7, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Maximum Speed [km/h]").grid(row=8, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Overhead Power [W]").grid(row=9, column=0, sticky=tkinter.W)


        ttk.Label(self, text=self.ev_obj.C_d).grid(row=2, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.A_front).grid(row=3, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.m).grid(row=4, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.payload_capacity).grid(row=5, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.curb_mass).grid(row=6, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.rot_mass).grid(row=7, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.max_speed).grid(row=8, column=1, sticky=tkinter.W)
        ttk.Label(self, text=self.ev_obj.overhead_power).grid(row=9, column=1, sticky=tkinter.W)


class ResultDisplay(MainDisplay):
    def __init__(self, parent_fme, text: str, parent_obj: tkinter.Frame) -> None:
        super().__init__(parent_fme=parent_fme, text=text, parent_obj=parent_obj)

    def create_power_demand_plot(self) -> None:
        if not isinstance(self.parent_obj, ResultInput):
            raise TypeError("parent_obj needs to be a ResultInput object.")
        tk_canvas = tkinter.Canvas(self)
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(self.parent_obj.sol.t, self.parent_obj.sol.battery_demand)
        ax.set_xlabel('Time [min]')
        ax.set_ylabel('Battery power demand [kW]')
        canvas = FigureCanvasTkAgg(figure=fig, master=tk_canvas)

        # Widget placement
        tk_canvas.grid(row=1, column=0)
        canvas.get_tk_widget().grid(row=0, column=0)


class DCParameterDisplay(ttk.Frame):
    MAX_ARRAY_LENGTH = 20

    def __init__(self, parent, user_selection, dc_obj):
        super().__init__(parent)

        if isinstance(dc_obj, EV_sim.DriveCycle):
            self.dc_obj = dc_obj
        else:
            raise TypeError("dc_obj needs to be a DriveCycle object.")

        if user_selection == InputAndDisplayFrames.lstbox_params_dc_choices[0]: # plot
            self.create_plot_display()
        elif user_selection == InputAndDisplayFrames.lstbox_params_dc_choices[1]: # array
            self.create_array_display()

        # Widget grid placement
        self.grid(row=0, column=0, sticky="news")

    def create_plot_display(self):
        tk_canvas = tkinter.Canvas(self)
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(figure=fig, master=tk_canvas)
        ax = fig.add_subplot()
        ax.plot(self.dc_obj.t, self.dc_obj.speed_kmph)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Speed [km/h]')

        # widget placement
        tk_canvas.grid(row=0, column=0, sticky="news")
        canvas.get_tk_widget().grid(row=0, column=0)

    def create_array_display(self):
        error_msg = tkinter.StringVar()

        if len(self.dc_obj.t) > self.MAX_ARRAY_LENGTH:
            max_length = self.MAX_ARRAY_LENGTH
            error_msg.set("Array too long. Results have been appended")
        else:
            max_length = len(self.dc_obj.t)

        ttk.Label(self, text="Time [s]").grid(row=0, column=0)
        ttk.Label(self, text="Speed [km/h]").grid(row=0, column=2)

        for row_i in range(0, max_length):
            ttk.Label(self, text=self.dc_obj.t[row_i]).grid(row=row_i+1, column=0)
            ttk.Label(self, text=self.dc_obj.speed_kmph[row_i]).grid(row=row_i + 1, column=2)

        ttk.Label(self, text=error_msg.get()).grid(row=self.MAX_ARRAY_LENGTH+5, column=0)


class ExtCondParameterDisplay(ttk.Frame):
    def __init__(self, parent, air_density, road_grade, road_force):
        super().__init__(parent)

        # variables
        self.error_msg = tkinter.StringVar()

        # Check for incomplete external conditions
        try:
            float(air_density)
        except:
            self.error_msg.set("Invalid Air Density. Indicate Air Density in the Inputs Section.")

        try:
            float(road_grade)
        except:
            self.error_msg.set("Invalid road grade. Indicate road grade in the Inputs Section.")

        try:
            float(road_force)
        except:
            self.error_msg.set("Invalid road force. Indicate road force in the Inputs Section.")

        # Widgets
        ttk.Label(self, text="Air Density, kg/m^3").grid(row=2, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Grade, %").grid(row=3, column=0, sticky=tkinter.W)
        ttk.Label(self, text="Road Force, N").grid(row=4, column=0, sticky=tkinter.W)

        ttk.Label(self, text=air_density).grid(row=2, column=1, sticky=tkinter.W, padx=10)
        ttk.Label(self, text=road_grade).grid(row=3, column=1, sticky=tkinter.W, padx=10)
        ttk.Label(self, text=road_force).grid(row=4, column=1, sticky=tkinter.W, padx=10)

        ttk.Label(self, text=self.error_msg.get(), foreground='red', font=VehicleDynamicsApp2.error_font_style)\
            .grid(row=5, column=0, columnspan=5)

        # Widget placement
        self.grid(row=0, column=0, sticky="news")


class ResultInput(ttk.Frame):
    lstbox_results_choices = ["Power demand"]

    def __init__(self, parent, start_row_num):
        super().__init__(parent)

        # Instance variables
        self.parent = parent
        self.start_row_num = start_row_num
        self.error_msg = tkinter.StringVar()

        self.var_lstbox_results = tkinter.StringVar()
        self.var_lstbox_results.set(self.lstbox_results_choices)

        # Widgets
        ttk.Label(self, text="Results", font= VehicleDynamicsApp2.heading_style).grid(row=0, column=0, sticky=tkinter.W)
        bttn_sim = ttk.Button(self, text="Simulate", command=self.simulate)

        # Widget grid placement
        bttn_sim.grid(row=start_row_num + 1, column=0, sticky=tkinter.W)
        self.grid(row=start_row_num, column=0, sticky=tkinter.W, pady=(10,0))

    def simulate(self):
        self.ev_obj = self.parent.ev_obj
        self.dc_obj = self.parent.dc_obj
        try:
            self.ext_cond_obj = EV_sim.ExternalConditions(rho= float(self.parent.var_air_pressure.get()),
                                                      road_grade=float(self.parent.var_road_grade.get()),
                                                      road_force=float(self.parent.var_road_force.get()))
            model = EV_sim.VehicleDynamics(ev_obj=self.ev_obj, drive_cycle_obj=self.dc_obj,
                                           external_condition_obj=self.ext_cond_obj)
            self.sol = model.simulate()

            self.lstbox_result = tkinter.Listbox(self, listvariable=self.var_lstbox_results, width=50,
                                                 selectmode="single", height=len(self.lstbox_results_choices),
                                                 exportselection=False)

            # bindings
            self.lstbox_result.bind('<<ListboxSelect>>', self.cmd_lstbox_result)

            # Widget placements
            self.lstbox_result.grid(row=self.start_row_num + 2, column=0)
        except:
            self.error_msg.set("Set valid external conditions.")
            ttk.Label(self, text=self.error_msg.get(), font= VehicleDynamicsApp2.error_font_style, foreground='red')\
                .grid(row=self.start_row_num+2, column=0)

    def cmd_lstbox_result(self, event):
        ResultDisplay(parent_fme=self.parent.fme_display, text=self.lstbox_results_choices[0], parent_obj=self)


if __name__ == '__main__':
    VehicleDynamicsApp2()
