#  Copyright (c) 2023. Moin Ahmed. All rights reserved.

import pandas as pd

try:
    import EV_sim
except ModuleNotFoundError:
    import sys
    import os

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    import EV_sim


alias_name = "Tesla_2022_Model3_RWD"
tesla = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.DriveCycle(drive_cycle_name="us06")
std_condition = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=udds, external_condition_obj=std_condition)
sol = model.simulate()

# plot
sol.plot()
