from tkinter import ttk
import glob

from EV_sim.gui.tkinter_variables import *


# GUI code begins here, using the Tk instance from the tkinter_variables module
# Styles
heading_style = ('Helvetica', 10, 'bold')
main_frame_styles = {'padding':"3 3 12 12", 'borderwidth': 2, 'relief': 'sunken'}

# Frame1: User Input
user_input_frame = ttk.Frame(root, padding="3 3 12 12", borderwidth=2, relief='sunken')
user_input_main_heading = ttk.Label(user_input_frame, text="User Input", font= heading_style)
## Sub-headings
user_input_subheading1 = ttk.Label(user_input_frame, text="EV Alias")
user_input_subheading2 = ttk.Label(user_input_frame, text="Drive Cycle")
user_input_subheading3 = ttk.Label(user_input_frame, text="Air Density, kg/m^3")
user_input_subheading4 = ttk.Label(user_input_frame, text= "Road Grade, %")
user_input_subheading5 = ttk.Label(user_input_frame, text="Road Force, N")
## User Entries
user_input_alias_combo = ttk.Combobox(user_input_frame, textvariable=var_EV_alias)
var_dc = tkinter.StringVar() # variable for the Drive Cycle
user_input_alias_combo['values'] = EV_sim.EV.list_all_EV_alias(file_dir=EV_DATABASE_DIR) # Adds all the EV alias to the ComboBox.
user_input_dc_combo = ttk.Combobox(user_input_frame, textvariable=var_dc)
user_input_dc_combo['values'] = all_dc
user_input_entry3 = ttk.Entry(user_input_frame)
user_input_entry4 = ttk.Entry(user_input_frame)
user_input_entry5 = ttk.Entry(user_input_frame)

# Frame 2: Parameter's Frame
parameter_main_frame = ttk.Frame(root, padding="3 3 12 12", borderwidth=2, relief='sunken')
## Motor Information
parameter_motor_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

motor_main_label = ttk.Label(parameter_motor_frame, text="Motor Information", font=heading_style)

motor_display_label1 = ttk.Label(parameter_motor_frame, text="Motor Type")
motor_display_label2 = ttk.Label(parameter_motor_frame, text="Rated Speed, RPM")
motor_display_label3 = ttk.Label(parameter_motor_frame, text="Max. Speed, RPM")
motor_display_label4 = ttk.Label(parameter_motor_frame, text="Max. Torque, Nm")
motor_display_label5 = ttk.Label(parameter_motor_frame, text="Efficiency")
motor_display_label6 = ttk.Label(parameter_motor_frame, text="Inertia, kg m^2")
motor_display_label7 = ttk.Label(parameter_motor_frame, text="Max. Power, kW")

motor_output_label1 = ttk.Label(parameter_motor_frame, textvariable=var_motor_type)
motor_output_label2 = ttk.Label(parameter_motor_frame, textvariable=var_motor_rated_speed)
motor_output_label3 = ttk.Label(parameter_motor_frame, textvariable=var_motor_max_speed)
motor_output_label4 = ttk.Label(parameter_motor_frame, textvariable=var_motor_max_torque)
motor_output_label5 = ttk.Label(parameter_motor_frame, textvariable=var_motor_eff)
motor_output_label6 = ttk.Label(parameter_motor_frame, textvariable=var_motor_inertia)
motor_output_label7 = ttk.Label(parameter_motor_frame, textvariable=var_motor_max_power)

### Wheel Information
parameter_wheel_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

wheel_main_label = ttk.Label(parameter_wheel_frame, text="Wheel Information", font=heading_style)

wheel_display_label1 = ttk.Label(parameter_wheel_frame, text="Radius, m")
wheel_display_label2 = ttk.Label(parameter_wheel_frame, text="Inertia, kg m^2")

wheel_output_label1 = ttk.Label(parameter_wheel_frame, textvariable=var_wheel_radius)
wheel_output_label2 = ttk.Label(parameter_wheel_frame, textvariable=var_wheel_inertia)

## Gearbox Information
parameter_gearbox_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

gearbox_main_label = ttk.Label(parameter_gearbox_frame, text="Gearbox Information", font=heading_style)

gearbox_display_label1 = ttk.Label(parameter_gearbox_frame, text="Gearbox Ratio")
gearbox_display_label2 = ttk.Label(parameter_gearbox_frame, text="Inertia, kg m^2")

gearbox_output_label1 = ttk.Label(parameter_gearbox_frame, textvariable=var_gearbox_N)
gearbox_output_label2 = ttk.Label(parameter_gearbox_frame, textvariable=var_gearbox_I)

## DriveTrain Information
parameter_dt_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

dt_main_label = ttk.Label(parameter_dt_frame, text="Drivetrain Information", font=heading_style)

dt_display_label1 = ttk.Label(parameter_dt_frame, text="No. wheels")
dt_display_label2 = ttk.Label(parameter_dt_frame, text="inverter Efficiency")
dt_display_label3 = ttk.Label(parameter_dt_frame, text="Fraction of regeneration")
dt_display_label4 = ttk.Label(parameter_dt_frame, text="Efficiency")

dt_output_label1 = ttk.Label(parameter_dt_frame, textvariable=var_dt_num_wheel)
dt_output_label2 = ttk.Label(parameter_dt_frame, textvariable=var_dt_inverter_eff)
dt_output_label3 = ttk.Label(parameter_dt_frame, textvariable=var_dt_frac_regen_torque)
dt_output_label4 = ttk.Label(parameter_dt_frame, textvariable=var_dt_eff)

## Battery Cell Information
parameter_batt_cell_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

battery_cell_main_label = ttk.Label(parameter_batt_cell_frame, text="Battery Cell Information", font=heading_style)

battery_cell_display_label1 = ttk.Label(parameter_batt_cell_frame, text="Cell Manufacturer")
battery_cell_display_label2 = ttk.Label(parameter_batt_cell_frame, text="Cell Capacity, Ah")
battery_cell_display_label3 = ttk.Label(parameter_batt_cell_frame, text="Cell Mass, g")
battery_cell_display_label4 = ttk.Label(parameter_batt_cell_frame, text="V. min., V")
battery_cell_display_label5 = ttk.Label(parameter_batt_cell_frame, text="V. nom, V")
battery_cell_display_label6 = ttk.Label(parameter_batt_cell_frame, text="V. min, V")
battery_cell_display_label7 = ttk.Label(parameter_batt_cell_frame, text="Cell Energy, Wh")
battery_cell_display_label8 = ttk.Label(parameter_batt_cell_frame, text="Cell Specific Energy, Wh/kg")

battery_cell_output_label1 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_manu)
battery_cell_output_label2 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_cap)
battery_cell_output_label3 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_mass)
battery_cell_output_label4 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_v_min)
battery_cell_output_label5 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_v_nom)
battery_cell_output_label6 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_v_max)
battery_cell_output_label7 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_energy)
battery_cell_output_label8 = ttk.Label(parameter_batt_cell_frame, textvariable=var_batt_cell_spec_energy)

## Battery Module Information
parameter_module_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

module_main_label = ttk.Label(parameter_module_frame, text="Battery Module Information", font=heading_style)

module_display_label1 = ttk.Label(parameter_module_frame, text="Ns")
module_display_label2 = ttk.Label(parameter_module_frame, text="Np")
module_display_label3 = ttk.Label(parameter_module_frame, text="Overhead Mass, %")
module_display_label4 = ttk.Label(parameter_module_frame, text="Tot. cells")
module_display_label5 = ttk.Label(parameter_module_frame, text="Capacity, Ah")
module_display_label6 = ttk.Label(parameter_module_frame, text="Mass, kg")
module_display_label7 = ttk.Label(parameter_module_frame, text="Energy, Whr")
module_display_label8 = ttk.Label(parameter_module_frame, text="Specific Energy, Wh")

module_output_label1 = ttk.Label(parameter_module_frame, textvariable=var_batt_module_ns)
module_output_label2 = ttk.Label(parameter_module_frame, textvariable=var_batt_module_np)
module_output_label3 = ttk.Label(parameter_module_frame, textvariable=var_batt_module_overhead_mass)
module_output_label4 = ttk.Label(parameter_module_frame, textvariable=var_tot_cells)
module_output_label5 = ttk.Label(parameter_module_frame, textvariable=var_module_cap)
module_output_label6 = ttk.Label(parameter_module_frame, textvariable=var_module_mass)
module_output_label7 = ttk.Label(parameter_module_frame, textvariable=var_module_energy)
module_output_label8 = ttk.Label(parameter_module_frame, textvariable=var_module_specific_energy)

## Battery Pack Information
parameter_pack_frame = ttk.Frame(parameter_main_frame, padding="3 3 12 12", borderwidth=2, relief='sunken')

pack_main_label = ttk.Label(parameter_pack_frame, text="Battery Module Information", font=heading_style)

pack_display_label1 = ttk.Label(parameter_pack_frame, text="Tot. Modules")
pack_display_label2 = ttk.Label(parameter_pack_frame, text="Mass, kg")
pack_display_label3 = ttk.Label(parameter_pack_frame, text="Energy, Wh")
pack_display_label4 = ttk.Label(parameter_pack_frame, text="Specific Energy, Ah/kg")
pack_display_label5 = ttk.Label(parameter_pack_frame, text="V. min., V")
pack_display_label6 = ttk.Label(parameter_pack_frame, text="V. nom., V")
pack_display_label7 = ttk.Label(parameter_pack_frame, text="V. max., V")

pack_output_label1 = ttk.Label(parameter_pack_frame, textvariable=var_pack_num_modules)
pack_output_label2 = ttk.Label(parameter_pack_frame, textvariable=var_pack_mass)
pack_output_label3 = ttk.Label(parameter_pack_frame, textvariable=var_pack_energy)
pack_output_label4 = ttk.Label(parameter_pack_frame, textvariable=var_module_specific_energy)
pack_output_label5 = ttk.Label(parameter_pack_frame, textvariable=var_pack_v_min)
pack_output_label6 = ttk.Label(parameter_pack_frame, textvariable=var_pack_v_nom)
pack_output_label7 = ttk.Label(parameter_pack_frame, textvariable=var_pack_v_max)

# grid
## Frame1
user_input_frame.grid(row=0, column=0, sticky=(tkinter.N, tkinter.W, tkinter.E))
user_input_main_heading.grid(row=0, column=0, sticky=tkinter.W)

user_input_subheading1.grid(row=1, column=0, sticky=tkinter.W)
user_input_subheading2.grid(row=2, column=0, sticky=tkinter.W)
user_input_subheading3.grid(row=3, column=0, sticky=tkinter.W)
user_input_subheading4.grid(row=4, column=0, sticky=tkinter.W)
user_input_subheading5.grid(row=5, column=0, sticky=tkinter.W)

user_input_alias_combo.grid(row=1, column=1)
user_input_dc_combo.grid(row=2, column=1)
user_input_entry3.grid(row=3, column=1)
user_input_entry4.grid(row=4, column=1)
user_input_entry5.grid(row=5, column=1)

## Frame2
parameter_main_frame.grid(row=0, column=3, sticky=(tkinter.N, tkinter.W, tkinter.E))
### Motor Information
parameter_motor_frame.grid(row=0, column=0, rowspan=2)
motor_main_label.grid(row=0, column=0)

motor_display_label1.grid(row=1, column=0, sticky=tkinter.W)
motor_display_label2.grid(row=2, column=0, sticky=tkinter.W)
motor_display_label3.grid(row=3, column=0,sticky=tkinter.W)
motor_display_label4.grid(row=4, column=0, sticky=tkinter.W)
motor_display_label5.grid(row=5, column=0, sticky=tkinter.W)
motor_display_label6.grid(row=6, column=0, sticky=tkinter.W)
motor_display_label7.grid(row=7, column=0, sticky=tkinter.W)

motor_output_label1.grid(row=1, column=1, rowspan=1)
motor_output_label2.grid(row=2, column=1)
motor_output_label3.grid(row=3, column=1)
motor_output_label4.grid(row=4, column=1)
motor_output_label5.grid(row=5, column=1)
motor_output_label6.grid(row=6, column=1)
motor_output_label7.grid(row=7, column=1)

### Wheel Information
parameter_wheel_frame.grid(row=0, column=1, sticky=tkinter.N)

wheel_main_label.grid(row=0, column=0)

wheel_display_label1.grid(row=1, column=0, sticky=tkinter.W)
wheel_display_label2.grid(row=2, column=0, sticky=tkinter.W)

wheel_output_label1.grid(row=1, column=1)
wheel_output_label2.grid(row=2, column=1)

### Gearbox Information
parameter_gearbox_frame.grid(row=1, column=1)

gearbox_main_label.grid(row=0, column=0)

gearbox_display_label1.grid(row=1, column=0, sticky=tkinter.W)
gearbox_display_label2.grid(row=2, column=0, sticky=tkinter.W)

gearbox_output_label1.grid(row=1, column=1)
gearbox_output_label2.grid(row=2, column=1)

### Drivetrain Information
parameter_dt_frame.grid(row=0, column=2, sticky=tkinter.N)

dt_main_label.grid(row=0, column=0)

dt_display_label1.grid(row=1, column=0, sticky=tkinter.W)
dt_display_label2.grid(row=2, column=0, sticky=tkinter.W)
dt_display_label3.grid(row=3, column=0, sticky=tkinter.W)
dt_display_label4.grid(row=4, column=0, sticky=tkinter.W)

dt_output_label1.grid(row=1, column=1)
dt_output_label2.grid(row=2, column=1)
dt_output_label3.grid(row=3, column=1)
dt_output_label4.grid(row=4, column=1)

## Battery Cell Information
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

## Battery Module Information
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

## Battery Pack Information
parameter_pack_frame.grid(row=2, column=3, sticky=tkinter.N)

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

# Widget Configurations
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
user_input_frame.rowconfigure(0, weight=1)
user_input_frame.rowconfigure(0, weight=1)
parameter_main_frame.rowconfigure(0, weight=1)
parameter_main_frame.columnconfigure(0, weight=1)

# Bindings
user_input_alias_combo.bind('<<ComboboxSelected>>', aliasComboboxCallbackFunc)

# Main loop
root.mainloop()

