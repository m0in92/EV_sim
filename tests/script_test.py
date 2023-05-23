from EV_sim.setup_vehicle import Cell, Module, Pack, Motor, Wheel, Drivetrain, Vehicle
from EV_sim.setup_drivecycles import Drive_cycle
from examples.sim import Sim
import pickle


vehicle_name = "Audi_e-tron_quattro_2019"
# veh1 = Basic_vehicle_info(vehicle_name)
# print(veh1.__dict__)
#
cell1 = Cell(vehicle_name)
print(cell1.__dict__)

mod1 = Module(vehicle_name)
print(mod1.__dict__)

pack1 = Pack(vehicle_name)
print(pack1.__dict__)

motor1 = Motor(vehicle_name)
print(motor1.__dict__)

wheel1 = Wheel(vehicle_name)
print(wheel1.__dict__)

dt1 = Drivetrain(vehicle_name)
print(dt1.__dict__)

veh1 = Vehicle(vehicle_name)
print(veh1.veh_equiv_mass)

drive_cycle_name = "hwfet"
dc = Drive_cycle(drive_cycle_name)
print(dc.speed_mps)
dc.plot()

a_file = open("../data/sim_params/sim_param.pkl", "rb")
sim_param = pickle.load(a_file)
print(sim_param)

sim1 = Sim(vehicle=veh1, drive_cycle=dc, sim_params=sim_param)
print(sim1.vehicle.__repr__())
print(sim1.drive_cycle.__repr__())
# print(type(sim1.rho))