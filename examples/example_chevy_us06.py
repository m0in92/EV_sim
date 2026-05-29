#  Copyright (c) 2023. Moin Ahmed. All rights reserved

try:
    import EV_sim
except ModuleNotFoundError:
    import sys
    import os

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    import EV_sim


alias_name = "Volt_2017"
volt = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.DriveCycle(drive_cycle_name="nycc")
waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
sol = model.simulate()

# plot
sol.plot()
