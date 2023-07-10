#  Copyright (c) 2023. Moin Ahmed. All rights reserved.

import EV_sim

import pandas as pd


alias_name = "Tesla_2022_Model3_RWD"
tesla = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.DriveCycle(drive_cycle_name="us06")
waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=udds, external_condition_obj=waterloo)
sol = model.simulate()

# plot
sol.plot()
