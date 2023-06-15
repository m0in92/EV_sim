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
from EV_sim.gui_dir.menubar import MenuBarClass
from EV_sim.tkinter_gui.sim_variables import InputSimVariables
from EV_sim.tkinter_gui.ribbon import Ribbon

# Global variables
icon_dir = os.path.join(definations.ROOT_DIR, 'gui_dir', 'icon.ico')

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
        self.geometry('1000x800')

        # instance variables
        self.var_lstbox_inputs_user_choice = tkinter.StringVar()
        self.set_two_decimal = tkinter.BooleanVar()  # option whether to show results in two decimal places.
        self.set_two_decimal.set(False)  # Initialize so that this option is False
        self.sim_vars = InputSimVariables()  # simulate variables instance

        # Style, only for the paned window scroll
        style = ttk.Style()
        style.theme_use('classic')

        # Widgets
        mb = MenuBarClass(self)  # menubar using the MenuBarClass below.
        rib = Ribbon(self)
        self.pw = ttk.PanedWindow(self, orient=tkinter.HORIZONTAL)  # PanedWindow Widget
        self.DisplayFrameInstance = MainDisplayFrame(self)  # Display Frame
        self.InputFrameInstance = MainInputFrame(self)  # Input Frame

        # Widget grid placements
        self.pw.add(self.InputFrameInstance)
        self.pw.add(self.DisplayFrameInstance)
        self.pw.grid(row=1, column=0, sticky="news")

        # Row and column configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.config(menu=mb)

        # main loop
        self.mainloop()


class MainInputFrame(ttk.Frame):
    lstbox_inputs_choices = {
        'Simulation Inputs': ["EV", "Drive Cycle", "External Conditions"]}  # all main choices in the input section
    lstbox_params_choices = {'Vehicle': ["Basic", "Cell", "Module", "Pack", "Motor", "Wheel", "Drivetrain", "Design"],
                             'Drive Cycle': ['plot'],
                             'External Conditions': ["values"]}
    lstbox_result_choices = {'Results': ["Desired Acceleration", "Desired Accelerating Force", "Aerodynamic Force",
                                         "Rolling Grade Force", "Demand Torque", "Max. Torque", "Limit Regeneration",
                                         "Limit Torque", "Motor Torque", "Actual Accelerating Force",
                                         "Actual Acceleration",
                                         "Motor Speed", "Actual Speed", "Distance", "Motor Demand Power", "Limit Power",
                                         "Battery Demand", "Battery Current"]}

    def __init__(self, parent):
        self.parent = parent  # parent instance
        super().__init__(self.parent)

        # Widgets
        SubInputFrame(self, fme_row=0, fme_col=0, main_heading_text="Inputs",
                      lstbox_choices=self.lstbox_inputs_choices)  # Input Frame
        SubInputFrame(self, fme_row=1, fme_col=0, main_heading_text="Parameters",
                      lstbox_choices=self.lstbox_params_choices)  # Parameters Frame
        SubInputFrame(self, fme_row=2, fme_col=0, main_heading_text='Simulation Results',
                      lstbox_choices=self.lstbox_result_choices)  # Result Frame

        # Widget Layout
        self.grid(row=1, column=0, sticky='news', rowspan=100)


class SubInputFrame(ttk.Frame):
    def __init__(self, parent: MainInputFrame, fme_row: int, fme_col: int, main_heading_text: str,
                 lstbox_choices: dict):
        self.parent = parent
        super().__init__(parent)

        # check for input types
        if not isinstance(main_heading_text, str):
            raise TypeError("Main heading text needs to be a string type.")
        if not isinstance(lstbox_choices, dict):
            raise TypeError("lst_box_choices needs to be an input type.")

        # Instance variables
        self.main_heading_text = main_heading_text
        self.lstbox_choices = lstbox_choices
        self.var_lstbox_choices = {}
        for category in self.lstbox_choices.keys():  # this iteration loop creates a tkinter variable for each listbox.
            self.var_lstbox_choices[category] = tkinter.StringVar()
            self.var_lstbox_choices[category].set(self.lstbox_choices[category])
        self.dict_lstbox_instances = {}  # this dict contains the instances of all list boxes. It is initialized here.
        self.user_selection = tkinter.StringVar()

        # Widgets
        ttk.Label(self, text=main_heading_text, font=VehicleDynamicsApp.heading_style).grid(row=0, column=0)
        self.create_widget()

        # Widget Layout
        self.grid(row=fme_row, column=fme_col)

        self.create_bindings()

    def create_widget(self):
        row_start_num = 1  # starting row index
        for category_index, category in enumerate(self.lstbox_choices.keys()):
            ttk.Label(self, text=category, font=VehicleDynamicsApp.heading_style2).grid(row=row_start_num, column=0,
                                                                                        sticky=tkinter.W)
            row_start_num += 1
            lstbox = tkinter.Listbox(self, width=50, listvariable=self.var_lstbox_choices[category],
                                     selectmode="single", exportselection=False,
                                     height=len(self.lstbox_choices[category]))
            lstbox.grid(row=row_start_num, column=0)
            row_start_num += 1

            exec('self.lstbox_' + category.replace(' ', '_') + '= lstbox')
            self.dict_lstbox_instances[category] = lstbox

    def create_bindings(self):
        for category in self.lstbox_choices.keys():
            exec('self.lstbox_' + category.replace(' ',
                                                   '_') + f".bind('<<ListboxSelect>>', lambda e:self.lstbox_callback(e,'{category}'))",
                 locals())

    def lstbox_callback(self, event, category):
        user_selection = event.widget.get(event.widget.curselection())
        self.parent.parent.DisplayFrameInstance.create_widget(self.main_heading_text + '-' + category +
                                                              '-' + user_selection, category=category,
                                                              user_selection=user_selection)


class MainDisplayFrame(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        # Widgets
        self.create_widget(main_heading_text="Default", category="Default", user_selection="Default")

        # Layout
        self.grid(row=1, column=1, sticky='news')

    @property
    def info_dict(self):
        if self.parent.sim_vars.ev_obj_instances[0].alias_name is not None:
            ev_obj = self.parent.sim_vars.ev_obj_instances[0]
            ev_pack_obj = ev_obj.pack
            ev_motor_obj = ev_obj.motor
            ev_wheel_obj = ev_obj.drive_train.wheel
            ev_dt_obj = ev_obj.drive_train
            info_dict = dict(Basic={'Model': ev_obj.model_name,
                                    'Manufacturer': ev_obj.manufacturer,
                                    'Year': ev_obj.year,
                                    'Trim:': ev_obj.trim},
                             Cell={'Manufacturer': ev_pack_obj.cell_manufacturer,
                                   'Chemistry': ev_pack_obj.cell_chem,
                                   "Capacity [A hr]": ev_pack_obj.cell_cap,
                                   'Mass [g]': ev_pack_obj.cell_mass,
                                   'V_max [V]': ev_pack_obj.cell_V_max,
                                   'V_nom [V]': ev_pack_obj.cell_V_nom,
                                   'V_min [V]': ev_pack_obj.cell_V_min,
                                   'Cell Energy, Wh': ev_pack_obj.cell_energy,
                                   'Cell Specific Energy, Wh/kg': ev_pack_obj.cell_spec_energy},
                             Module={'No. of parallel cells]': ev_pack_obj.Np,
                                     'No. of series cells]': ev_pack_obj.Ns,
                                     'No. of tot. cells': ev_pack_obj.total_no_cells,
                                     'Overhead mass ratio': ev_pack_obj.module_overhead_mass,
                                     'Capacity [Ah]': ev_pack_obj.module_cap,
                                     'Mass [kg]': ev_pack_obj.module_mass,
                                     'Energy [kWh]': ev_pack_obj.module_energy,
                                     'Specific Energy [Wh/kg]': ev_pack_obj.module_specific_energy},
                             Pack={'Tot. Modules': ev_pack_obj.num_modules,
                                   'Mass, kg': ev_pack_obj.pack_mass,
                                   'Energy, Wh': ev_pack_obj.pack_energy,
                                   'Specific Energy, Wh/kg': ev_pack_obj.pack_specific_energy,
                                   'Minimum Potential, V': ev_pack_obj.pack_V_min,
                                   'Nominal Potential, V': ev_pack_obj.pack_V_nom,
                                   'Maximum Potential, V': ev_pack_obj.pack_V_max},
                             Motor={'Motor Type': ev_motor_obj.motor_type,
                                    'Rated Speed, RPM': ev_motor_obj.RPM_r,
                                    'Max. Speed, RPM': ev_motor_obj.RPM_max,
                                    'Max. Torque, Nm': ev_motor_obj.L_max,
                                    'Efficiency': ev_motor_obj.eff,
                                    'Inertia, kg m^2': ev_motor_obj.I,
                                    'Max. Power, kW': ev_motor_obj.P_max},
                             Wheel={'Radius, m': ev_wheel_obj.r,
                                    'Inertia, kg m^2': ev_wheel_obj.I},
                             Drivetrain={'Gearbox Ratio': ev_dt_obj.gear_box.N,
                                         'Gearbox Inertia, kg m^2': ev_dt_obj.gear_box.I,
                                         'No. wheels': ev_dt_obj.num_wheel,
                                         'inverter Efficiency': ev_dt_obj.inverter_eff,
                                         'Fraction of regeneration': ev_dt_obj.frac_regen_torque,
                                         'Efficiency': ev_dt_obj.eff},
                             Design={
                                 'Drag Coefficient': ev_obj.C_d,
                                 'Frontal Area, m^2': ev_obj.A_front,
                                 'Mass [kg]': ev_obj.m,
                                 'Payload Cap [kg]': ev_obj.payload_capacity,
                                 'Curb Mass [kg]': ev_obj.curb_mass,
                                 'Rotational Mass [kg]")': ev_obj.rot_mass,
                                 'Maximum Speed [km/h]")': ev_obj.max_speed,
                                 'Overhead Power [W]")': ev_obj.overhead_power
                             })

            return info_dict
        else:
            return dict(Basic={}, Cell={}, Module={}, Pack={}, Motor={}, Wheel={}, Drivetrain={}, Design={})

    @property
    def info_ext_cond_dict(self):
        ext_cond_obj = self.parent.sim_vars.ext_cond_obj
        return {'Air Density, kg/m^3': ext_cond_obj.rho, 'Road Grade, %': ext_cond_obj.road_grade,
                'Road Force, N' : ext_cond_obj.road_force}

    def create_widget(self, main_heading_text: str, category: str, user_selection: str):
        """
        Catetorgoies are (1) Simulation Inputs
        :param main_heading_text:
        :param category:
        :return:
        """
        ttk.Frame(self).grid(row=0, column=0, sticky='news')
        ttk.Label(self, text=main_heading_text, font=VehicleDynamicsApp.heading_style) \
            .grid(row=0, column=0, sticky=(tkinter.N, tkinter.W))
        if category == 'Simulation Inputs':
            if user_selection == 'EV':
                SubDisplayComboBox(self, cmbbox_options={
                    'EV_Alias': EV_sim.EVFromDatabase.list_all_EV_alias(file_dir=VehicleDynamicsApp.EV_DATABASE_DIR)},
                                   user_selection=user_selection)
            elif user_selection == 'Drive Cycle':
                dc_wildcard_txt = definations.ROOT_DIR + '\data\drive_cycles\*.txt'
                SubDisplayComboBox(self, cmbbox_options={
                    'Drive Cycle': [os.path.split(file_)[-1].split('.')[0] for file_ in glob.glob(dc_wildcard_txt)]},
                                   user_selection=user_selection)
            elif user_selection == 'External Conditions':
                SubDisplayUserEntry(self, entry_list=["Air Density, kg/m^3", "Road Grade, %", "Road Force, N"])
        elif category == 'Vehicle':
            SubDisplayParameters(self, self.info_dict[user_selection])
        elif category == 'Drive Cycle':
            SubDisplayPlots(self, user_selection=user_selection)
        elif category == 'External Conditions':
            SubDisplayParameters(self, self.info_ext_cond_dict)
        elif category == 'Results':
            SubDisplayPlots(self, user_selection=user_selection)


class SubDisplayComboBox(ttk.Frame):
    def __init__(self, parent, cmbbox_options: dict, user_selection: str):
        self.parent = parent
        if not isinstance(user_selection, str):
            raise TypeError('user selection needs to be a string object.')
        self.user_selection = user_selection
        super().__init__(self.parent)

        # instance variables
        self.cmbbox_options = cmbbox_options

        self.create_widgets()
        self.create_bindings()
        self.grid(row=1, column=0, sticky='news')  # Frame layout

    def create_widgets(self):
        row_num = 0  # row number for the grid
        for label_ in self.cmbbox_options.keys():
            ttk.Label(self, text=label_).grid(row=row_num, column=0)

            cmbbox_name = 'self.cmbbox_' + label_.replace(' ', '_')
            exec(cmbbox_name + '= ttk.Combobox(self)')
            exec(cmbbox_name + "['values'] = self.cmbbox_options[label_]")
            exec(cmbbox_name + '.grid(row=row_num, column=1, padx=10, pady=10)')

            row_num += 1  # update row_num for other combobox

    def create_bindings(self):
        for label_ in self.cmbbox_options.keys():
            cmbbox_name = 'self.cmbbox_' + label_.replace(' ', '_')
            exec(cmbbox_name + ".bind('<<ComboboxSelected>>', self.cmbbox_callback)")

    def cmbbox_callback(self, event) -> None:
        user_selection_cmbbox = event.widget.get()
        if self.user_selection == 'EV':
            self.parent.parent.sim_vars.update_EV_instance(instance_index=0, alias_name=user_selection_cmbbox)
        elif self.user_selection == 'Drive Cycle':
            self.parent.parent.sim_vars.update_drivecycle_instance(drive_cycle_name=user_selection_cmbbox)


class SubDisplayUserEntry(ttk.Frame):
    def __init__(self, parent, entry_list: list):
        self.parent = parent
        if not isinstance(entry_list, list):
            raise TypeError('Entry dict needs to be a dict type.')
        self.entry_list = entry_list

        super().__init__(self.parent)
        self.create_widget()
        self.create_bindings()
        self.grid(row=1, column=0, sticky='news')  # Frame layout

    def create_widget(self):
        row_num = 0
        for label_ in self.entry_list:
            ttk.Label(self, text=label_).grid(row=row_num, column=0, sticky=tkinter.W, pady=10, padx=10)
            entry_name = 'self.' + label_.replace(' ', '_').replace(',', '').replace('/', '').replace('^', '').replace(
                '%', '')
            exec(entry_name + "=ttk.Entry(self, text=label_)")
            exec(entry_name + '.grid(row=row_num, column=1)')
            row_num += 1

    def create_bindings(self):
        for label_ in self.entry_list:
            entry_name = 'self.' + label_.replace(' ', '_').replace(',', '').replace('/', '').replace('^', '').replace(
                '%', '')
            exec(entry_name + ".bind('<KeyRelease>', self.entry_callback)")

    def entry_callback(self, event):
        user_input = event.widget.get()
        if user_input:
            if event.widget['text'] == self.entry_list[0]:  # Air pressure or rho
                self.parent.parent.sim_vars.update_rho(float(user_input))
            elif event.widget['text'] == self.entry_list[1]:  # Road grade
                self.parent.parent.sim_vars.update_road_grade(float(user_input))
            elif event.widget['text'] == self.entry_list[2]:  # Road force
                self.parent.parent.sim_vars.update_road_force(float(user_input))


class SubDisplayParameters(ttk.Frame):
    def __init__(self, parent, info_dict):
        self.parent = parent
        if not isinstance(info_dict, dict):
            raise TypeError("Info_dict needs to be a dict.")
        self.info_dict = info_dict

        super().__init__(parent)

        self.create_widget()
        self.create_bindings()

        self.grid(row=1, column=0, sticky='news')  # Frame layout

    def create_widget(self):
        row_num = 0
        for label_ in self.info_dict.keys():
            ttk.Label(self, text=label_).grid(row=row_num, column=0, sticky=tkinter.W, padx=10, pady=5)
            ttk.Label(self, text=self.info_dict[label_]).grid(row=row_num, column=1, sticky=tkinter.W, padx=10, pady=5)
            row_num += 1

    def create_bindings(self):
        pass


class SubDisplayPlots(ttk.Frame):
    def __init__(self, parent, user_selection: str):
        self.parent = parent
        if not isinstance(user_selection, str):
            raise TypeError('user_selection needs to be a string type.')
        self.user_selection = user_selection
        super().__init__(self.parent)

        self.create_widget()

        self.grid(row=1, column=0, sticky='news')  # Frame layout

    def create_widget(self):
        if self.user_selection == 'plot':
            if self.parent.parent.sim_vars.dc_obj.drive_cycle_name is not None:
                self.create_plot(x_values=self.parent.parent.sim_vars.dc_obj.t,
                                 y_values=self.parent.parent.sim_vars.dc_obj.speed_kmph,
                                 x_label = 'Time [min]', y_label='Speed [km/h]')

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
