from setup_vehicle import Basic_vehicle_info,Cell, Module, Pack, Motor, Wheel, Drivetrain, Vehicle
from setup_drivecycles import Drive_cycle
from sim import Sim
import pickle
import matplotlib.pyplot as plt


vehicle_name = "Volt_2017"
veh1 = Vehicle(vehicle_name)
drive_cycle_name = "us06"
dc = Drive_cycle(drive_cycle_name)
a_file = open("data/sim_params/sim_param.pkl", "rb")
sim_param = pickle.load(a_file)

sim1 = Sim(vehicle=veh1, drive_cycle=dc, sim_params=sim_param)
des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque, limit_regen, limit_torque, \
motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed, actual_speed_kmph, distance, \
motor_power, limit_power, battery_demand, current, battery_SOC = sim1.simulate()
# -----------------------------------
# trouble-shooting
# -----------------------------------
# print(sim1.des_speed) # checked
# print(des_acc) # checked
# print(des_acc_F) # checked
# print(aero_F) # checked
# print(roll_grade_F) # checked
# print(demand_torque) # checked
# print(max_torque) # checked
# print(limit_regen[20]) # checked
# print(limit_torque) # checked
# print(motor_torque) # checked
# print(actual_acc_F) # checked
# print(actual_acc) # checked
# print(motor_speed) # checked
# print(actual_speed)
# print(actual_speed_kmph)
# print(distance)
print(motor_power)

plt.plot(dc.time_s/60, battery_demand)
plt.xlabel('Time [min]')
plt.ylabel('Battery power demand [kW]')
plt.title('EV example drive cycle results')
plt.show()
