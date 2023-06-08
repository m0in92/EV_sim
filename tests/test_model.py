import sys
import unittest

import numpy as np

import EV_sim


np.set_printoptions(threshold=sys.maxsize)

class TestVehicleDynamics(unittest.TestCase):
    drive_cycle_name = "udds"
    def test_des_speed(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        self.assertEqual(1.341120000000000, model.des_speed[21])
        self.assertEqual(14.484096000000000, model.des_speed[113])
        self.assertAlmostEqual(0.983488000000000, model.des_speed[124])

    def test_sim_desired_acceleration(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired accelerations.
        self.assertEqual(1.341120000000000, sol.des_acc[21])
        self.assertAlmostEqual(1.296416000000000, sol.des_acc[22])
        self.assertAlmostEqual(-0.938784000000000, sol.des_acc[39])
        self.assertEqual(-1.475232000000000, sol.des_acc[119])
        self.assertAlmostEqual(1.430527999999997, sol.des_acc[194])

    def test_sim_acceleration_force(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired acceleration force.
        self.assertAlmostEqual(2.966052883762201e+03, sol.des_acc_F[21])
        self.assertEqual(7.909474356699195e+02, sol.des_acc_F[28])
        self.assertEqual(-3.262658172138421e+03, sol.des_acc_F[119])

    def test_sim_aero_force(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired areodynamic drag.
        self.assertAlmostEqual(0.445945591719936, sol.aero_F[22])
        self.assertEqual(23.981962932494340, sol.aero_F[119])

    def test_roll_grade_force(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the desired roll grade force.
        self.assertEqual(48.751215402632994, sol.roll_grade_F[20])
        self.assertAlmostEqual(2.291315240982852e+02, sol.roll_grade_F[119])

    def test_sim_demand_torque(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the demand torque.
        self.assertAlmostEqual(1.421910449243462, sol.demand_torque[0])
        self.assertEqual(-87.778386648972870, sol.demand_torque[119])

    def test_sim_max_torque(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the max. torque
        self.assertEqual(275, sol.max_torque[0])
        self.assertEqual(2.732933241759195e+02, sol.max_torque[84])
        self.assertEqual(275.0, sol.max_torque[119])

    def test_sim_limit_regeneration(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the limit regeneration
        self.assertEqual(2.475000000000000e+02, sol.limit_regen[0])
        self.assertEqual(2.363385665043329e+02, sol.limit_regen[112])
        self.assertEqual(2.475000000000000e+02, sol.limit_regen[119])

    def test_sim_limit_torque(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the limit torque
        self.assertAlmostEqual(1.421910449243462, sol.limit_torque[0])
        self.assertAlmostEqual(-87.778386648972870, sol.limit_torque[119])

    def test_sim_motor_torque(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the motor torque
        self.assertAlmostEqual(1.421910449243462, sol.motor_torque[0])
        self.assertEqual(87.931786225640980, sol.motor_torque[21])
        self.assertEqual(-87.778386648972870, sol.motor_torque[119])

    def test_sim_actual_acceleration_force(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the actual acceleration force
        self.assertEqual(0.0, sol.actual_acc_F[0])
        self.assertEqual(2.966052883762201e+03, sol.actual_acc_F[21])
        self.assertAlmostEqual(-3.262658172138421e+03, sol.actual_acc_F[119])

    def test_sim_actual_acceleration(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the actual acceleration
        self.assertEqual(0.0, sol.actual_acc[0])
        self.assertAlmostEqual(1.341120000000000, sol.actual_acc[21])
        self.assertAlmostEqual(-1.475232000000000, sol.actual_acc[119])

    def test_sim_motor_speed(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the motor speed
        self.assertEqual(0.0, sol.motor_speed[0])
        self.assertEqual(4.390886618319142e+02, sol.motor_speed[21])
        self.assertEqual(2.736985992085598e+03, sol.motor_speed[119])

    def test_sim_actual_speed(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the actual speed
        self.assertEqual(0.0, sol.actual_speed[0])
        self.assertEqual(1.341120000000000, sol.actual_speed[21])
        self.assertEqual(8.359648000000000, sol.actual_speed[119])

    def test_sim_demand_power(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the demand power
        self.assertEqual(0.0, sol.demand_power[0])
        self.assertEqual(2.021607036735971, sol.demand_power[21])
        self.assertEqual(-27.378622520221082, sol.demand_power[119])

    def test_sim_limit_power(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the limit power
        self.assertEqual(0.0, sol.limit_power[0])
        self.assertEqual(2.021607036735971, sol.limit_power[21])
        self.assertEqual(-27.378622520221082, sol.limit_power[119])

    def test_battery_demand(self):
        alias_name = "Volt_2017"
        volt = EV_sim.EVFromDatabase(alias_name=alias_name)
        udds = EV_sim.DriveCycle(drive_cycle_name=self.drive_cycle_name)
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        model = EV_sim.VehicleDynamics(ev_obj=volt, drive_cycle_obj=udds, external_condition_obj=waterloo)
        sol = model.simulate()
        # The lines below test for the battery demand
        self.assertEqual(0.2, sol.battery_demand[0])
        # self.assertEqual(2.631097151114207, sol.battery_demand[21])
        self.assertAlmostEqual(-22.567011148711070, sol.battery_demand[119], places=2)
