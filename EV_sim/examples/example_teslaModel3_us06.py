import matplotlib.pyplot as plt

import EV_sim


alias_name = "Tesla_2022_Model3_RWD"
tesla = EV_sim.EVFromDatabase(alias_name=alias_name)
udds = EV_sim.DriveCycle(drive_cycle_name="us06")
waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=udds, external_condition_obj=waterloo)
sol = model.simulate()

print(sol.t, sol.current/tesla.pack.Np)
print(max(sol.current/tesla.pack.Np))

# plot
sol.plot()