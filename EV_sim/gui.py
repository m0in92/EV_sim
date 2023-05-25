import tkinter
from tkinter import ttk

# from EV_sim.ev import EV
import EV_sim


# All important file directories
EV_DATABASE_DIR = "../data/EV/EV_dataset.csv"

# GUI code begins here


# Callback functions
def aliasComboboxCallbackFunc(event):
    user_input_alias_combo = event.widget.get()
    # initiate EV instance and update GUI variables
    ev_instance = EV_sim.EV(user_input_alias_combo)

    var_motor_type.set('AC Induction Motor')  # TO DO: Add more motor types.
    var_motor_rated_speed.set(ev_instance.motor.RPM_r)
    var_motor_max_speed.set(ev_instance.motor.RPM_max)
    var_motor_max_torque.set(ev_instance.motor.L_max)
    var_motor_eff.set(ev_instance.motor.eff)
    var_motor_inertia.set(ev_instance.motor.I)
    var_motor_max_power.set(ev_instance.motor.P_max)

    var_wheel_radius.set(ev_instance.drive_train.wheel.r)
    var_wheel_inertia.set(ev_instance.drive_train.wheel.I)

    var_gearbox_N.set(ev_instance.drive_train.gear_box.N)
    var_gearbox_I.set(ev_instance.drive_train.gear_box.I)


root = tkinter.Tk()
root.title("EV Simulator.")

# Relevant tkinter variables
var_EV_alias = tkinter.StringVar() # variable for the EV alias

var_motor_type = tkinter.StringVar()
var_motor_rated_speed = tkinter.StringVar()
var_motor_max_speed = tkinter.StringVar()
var_motor_max_torque = tkinter.StringVar()
var_motor_eff = tkinter.StringVar()
var_motor_inertia = tkinter.StringVar()
var_motor_max_power = tkinter.StringVar()

var_wheel_radius = tkinter.StringVar()
var_wheel_inertia = tkinter.StringVar()

var_gearbox_N = tkinter.StringVar() # gearbox ratio
var_gearbox_I = tkinter.StringVar() # gearbox inertia

# Styles
heading_style = ('Helvetica', 10, 'bold')

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






# frm1 = ttk.Frame(root)
# frm2 = ttk.Frame(frm1, borderwidth=5, relief="ridge", width=200, height=100)
# namelbl = ttk.Label(frm1, text="Name")
# name = ttk.Entry(frm1)
#
# onevar = tkinter.BooleanVar(value=True)
# twovar = tkinter.BooleanVar(value=False)
# threevar = tkinter.BooleanVar(value=True)
#
# one = ttk.Checkbutton(frm1, text="one", variable=onevar, onvalue=True)
# two = ttk.Checkbutton(frm1, text="one", variable=twovar, onvalue=True)
# three = ttk.Checkbutton(frm1, text="one", variable=threevar, onvalue=True)
# ok = ttk.Button(frm1, text="Okay")
# cancel = ttk.Button(frm1, text="Cancel")
#
# frm1.grid(column=0,row=0, sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
# frm2.grid(column=0, row=0, columnspan=3, rowspan=2)
# namelbl.grid(column=3, row=0, columnspan=2, sticky=(tkinter.W, tkinter.N), padx=5)
# name.grid(column=3, row=1, columnspan=2, sticky=(tkinter.N, tkinter.W, tkinter.E), padx=5, pady=5)
# one.grid(column=0, row=3)
# two.grid(column=1, row=3)
# three.grid(column=2, row=3)
# ok.grid(column=3, row=3)
# cancel.grid(column=4, row=3)
#
# root.columnconfigure(0, weight=1) # resizes the root
# root.rowconfigure(0, weight=1) # resizes the root
# frm1.columnconfigure(0, weight=3)
# frm1.columnconfigure(1, weight=3)
# frm1.columnconfigure(2, weight=3)
# frm1.columnconfigure(3, weight=1)
# frm1.columnconfigure(4, weight=1)
# frm1.rowconfigure(1, weight=1)
#
# root.mainloop()
