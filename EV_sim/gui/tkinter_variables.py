import tkinter
import glob

import EV_sim


# All important file directories
EV_DATABASE_DIR = "../../data/EV/EV_dataset.csv"

def aliasComboboxCallbackFunc(event):
    user_input_alias_combo = event.widget.get()
    # initiate EV instance and update GUI variables
    ev_instance = EV_sim.EV(user_input_alias_combo, database_dir=EV_DATABASE_DIR)

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

    var_dt_num_wheel.set(ev_instance.drive_train.num_wheel)
    var_dt_inverter_eff.set(ev_instance.drive_train.inverter_eff)
    var_dt_frac_regen_torque.set(ev_instance.drive_train.frac_regen_torque)
    var_dt_eff.set(ev_instance.drive_train.eff)

    var_batt_cell_manu.set(ev_instance.pack.cell_manufacturer)
    var_batt_cell_cap.set(ev_instance.pack.cell_cap)
    var_batt_cell_mass.set(ev_instance.pack.cell_mass)
    var_batt_cell_v_min.set(ev_instance.pack.cell_V_min)
    var_batt_cell_v_nom.set(ev_instance.pack.cell_V_nom)
    var_batt_cell_v_max.set(ev_instance.pack.cell_V_max)
    var_batt_cell_energy.set(ev_instance.pack.cell_energy)
    var_batt_cell_spec_energy.set(ev_instance.pack.cell_spec_energy)

    var_batt_module_ns.set(ev_instance.pack.Ns)
    var_batt_module_np.set(ev_instance.pack.Np)
    var_batt_module_overhead_mass.set(ev_instance.pack.module_overhead_mass)
    var_tot_cells.set(ev_instance.pack.total_no_cells)
    var_module_cap.set(ev_instance.pack.module_cap)
    var_module_mass.set(ev_instance.pack.module_mass)
    var_module_energy.set(ev_instance.pack.module_energy)
    var_module_specific_energy.set(ev_instance.pack.module_specific_energy)

    var_pack_num_modules.set(ev_instance.pack.num_modules)
    var_pack_mass.set(ev_instance.pack.pack_mass)
    var_pack_energy.set(ev_instance.pack.pack_energy)
    var_pack_specific_energy.set(ev_instance.pack.pack_specific_energy)
    var_pack_v_max.set(ev_instance.pack.pack_V_max)
    var_pack_v_nom.set(ev_instance.pack.pack_V_nom)
    var_pack_v_min.set(ev_instance.pack.pack_V_min)

# Intialize the Tk instance since the Tkinter definitions needs to come after it.
root = tkinter.Tk()
root.title("EV Simulator")

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

var_dt_num_wheel = tkinter.StringVar() # number of wheels in the vehicle
var_dt_inverter_eff = tkinter.StringVar() # inverter eff.
var_dt_frac_regen_torque = tkinter.StringVar() # fraction of regenerated torque
var_dt_eff = tkinter.StringVar() # drivetrain efficiency

var_batt_cell_manu = tkinter.StringVar()
var_batt_cell_cap = tkinter.StringVar() # battery cell capacity
var_batt_cell_mass = tkinter.StringVar()
var_batt_cell_v_max = tkinter.StringVar()
var_batt_cell_v_nom = tkinter.StringVar()
var_batt_cell_v_min = tkinter.StringVar()
var_batt_cell_energy = tkinter.StringVar()
var_batt_cell_spec_energy = tkinter.StringVar()

var_batt_module_ns = tkinter.StringVar()
var_batt_module_np = tkinter.StringVar()
var_batt_module_overhead_mass = tkinter.StringVar()
var_tot_cells = tkinter.StringVar()
var_module_cap = tkinter.StringVar()
var_module_mass = tkinter.StringVar()
var_module_energy = tkinter.StringVar()
var_module_specific_energy = tkinter.StringVar()

var_pack_num_modules = tkinter.StringVar()
var_pack_mass = tkinter.StringVar()
var_pack_energy = tkinter.StringVar()
var_pack_specific_energy = tkinter.StringVar()
var_pack_v_max = tkinter.StringVar()
var_pack_v_nom = tkinter.StringVar()
var_pack_v_min = tkinter.StringVar()

# Possible combo box
all_dc = [file_.split('\\')[1].split('.')[0] for file_ in glob.glob('../../data/drive_cycles/*.txt')]
