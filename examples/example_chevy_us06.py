import EV_sim


alias_name = "Volt_2017"
volt = EV_sim.EV(alias_name=alias_name)
udds = EV_sim.DriveCycle(drive_cycle_name="us06")
waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
sol = model.simulate()

# plot
sol.plot(t_array=udds.t, veh_alias_name=alias_name)