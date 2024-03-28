#  Copyright (c) 2024. Moin Ahmed. All Rights Reserved.

import matplotlib.pyplot as plt

import EV_sim
from EV_sim.sol import Solution

alias_name_tesla: str = "Tesla_2022_Model3_RWD"
alias_name_porshe: str = "Porsche_2020_Taycan4S"

tesla: EV_sim.EV = EV_sim.EVFromDatabase(alias_name=alias_name_tesla)
porche: EV_sim.EV = EV_sim.EVFromDatabase(alias_name=alias_name_porshe)

us06: EV_sim.DriveCycle = EV_sim.DriveCycle(drive_cycle_name="us06")
hwfet: EV_sim.DriveCycle = EV_sim.DriveCycle(drive_cycle_name="hwfet")
udds: EV_sim.DriveCycle = EV_sim.DriveCycle(drive_cycle_name="udds")
nycc: EV_sim.DriveCycle = EV_sim.DriveCycle(drive_cycle_name="nycc")
ftp: EV_sim.DriveCycle = EV_sim.DriveCycle(drive_cycle_name="ftp")
bcdc: EV_sim.DriveCycle = EV_sim.DriveCycle(drive_cycle_name="bcdc")

std_condition: EV_sim.ExternalConditions = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)

tesla_model_us06: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=us06,
                                                                  external_condition_obj=std_condition)
tesla_model_hwfet: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=hwfet,
                                                                   external_condition_obj=std_condition)
tesla_model_udds: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=udds,
                                                                  external_condition_obj=std_condition)
tesla_model_nycc: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=nycc,
                                                                  external_condition_obj=std_condition)
tesla_model_ftp: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=ftp,
                                                                 external_condition_obj=std_condition)
tesla_model_bcdc: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=tesla, drive_cycle_obj=bcdc,
                                                                  external_condition_obj=std_condition)

porche_model_us06: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=porche, drive_cycle_obj=us06,
                                                                   external_condition_obj=std_condition)
porche_model_hwfet: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=porche, drive_cycle_obj=hwfet,
                                                                    external_condition_obj=std_condition)
porche_model_udds: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=porche, drive_cycle_obj=udds,
                                                                   external_condition_obj=std_condition)
porche_model_nycc: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=porche, drive_cycle_obj=nycc,
                                                                   external_condition_obj=std_condition)
porche_model_ftp: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=porche, drive_cycle_obj=ftp,
                                                                  external_condition_obj=std_condition)
porche_model_bcdc: EV_sim.VehicleDynamics = EV_sim.VehicleDynamics(ev_obj=porche, drive_cycle_obj=bcdc,
                                                                   external_condition_obj=std_condition)

tesla_sol_us06: Solution = tesla_model_us06.simulate()
tesla_sol_hwfet: Solution = tesla_model_hwfet.simulate()
tesla_sol_udds: Solution = tesla_model_udds.simulate()
tesla_sol_nycc: Solution = tesla_model_nycc.simulate()
tesla_sol_ftp: Solution = tesla_model_ftp.simulate()
tesla_sol_bcdc: Solution = tesla_model_bcdc.simulate()

porche_sol_us06: Solution = porche_model_us06.simulate()
porche_sol_hwfet: Solution = porche_model_hwfet.simulate()
porche_sol_udds: Solution = porche_model_udds.simulate()
porche_sol_nycc: Solution = porche_model_nycc.simulate()
porche_sol_ftp: Solution = porche_model_ftp.simulate()
porche_sol_bcdc: Solution = porche_model_bcdc.simulate()

# plot
fig = plt.figure(figsize=(10 / 1.5, 12.5 / 1.5))
ax1 = fig.add_subplot(321)
ax1.plot(tesla_sol_us06.t, tesla_sol_us06.battery_demand, label='Tesla Model 3')
ax1.plot(porche_sol_us06.t, porche_sol_us06.battery_demand, '--', label='Porsche Taycan')
ax1.set_xlabel('Time [min]')
ax1.set_ylabel('Battery power demand [kW]')
ax1.set_title('US06')

ax2 = fig.add_subplot(322)
ax2.plot(tesla_sol_hwfet.t, tesla_sol_hwfet.battery_demand, label='Tesla Model 3')
ax2.plot(porche_sol_hwfet.t, porche_sol_hwfet.battery_demand, '--', label='Porsche Taycan')
ax2.set_xlabel('Time [min]')
ax2.set_ylabel('Battery power demand [kW]')
ax2.set_title('HWFET')

ax3 = fig.add_subplot(323)
ax3.plot(tesla_sol_udds.t, tesla_sol_udds.battery_demand, label='Tesla Model 3')
ax3.plot(porche_sol_udds.t, porche_sol_udds.battery_demand, '--', label='Porsche Taycan')
ax3.set_xlabel('Time [min]')
ax3.set_ylabel('Battery power demand [kW]')
ax3.set_title('UDDS')

ax4 = fig.add_subplot(324)
ax4.plot(tesla_sol_nycc.t, tesla_sol_nycc.battery_demand, label='Tesla Model 3')
ax4.plot(porche_sol_nycc.t, porche_sol_nycc.battery_demand, '--', label='Porsche Taycan')
ax4.set_xlabel('Time [min]')
ax4.set_ylabel('Battery power demand [kW]')
ax4.set_title('NYCC')

ax5 = fig.add_subplot(325)
ax5.plot(tesla_sol_ftp.t, tesla_sol_ftp.battery_demand, label='Tesla Model 3')
ax5.plot(porche_sol_ftp.t, porche_sol_ftp.battery_demand, '--', label='Porsche Taycan')
ax5.set_xlabel('Time [min]')
ax5.set_ylabel('Battery power demand [kW]')
ax5.set_title('FTP')

ax6 = fig.add_subplot(326)
ax6.plot(tesla_sol_bcdc.t, tesla_sol_bcdc.battery_demand, label='Tesla Model 3')
ax6.plot(porche_sol_bcdc.t, porche_sol_bcdc.battery_demand, '--', label='Porsche Taycan')
ax6.set_xlabel('Time [min]')
ax6.set_ylabel('Battery power demand [kW]')
ax6.set_title('FTP')

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25),
           fancybox=True, shadow=True, ncol=5)
plt.tight_layout()
plt.show()
