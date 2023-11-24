import EV_sim

import pandas as pd


alias_name = "Porsche_2020_Taycan4S"
porsche = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.DriveCycle(drive_cycle_name="us06")
std_condition = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.VehicleDynamics(ev_obj=porsche, drive_cycle_obj=udds, external_condition_obj=std_condition)
sol = model.simulate()

# plot
sol.plot()
