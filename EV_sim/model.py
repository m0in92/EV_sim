"""
This modules contains the classes and functionailities the calculations involved with the electric vehicle dynamic
simulations
"""

__all__ = ['VehicleDynamics']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by EV_sim. All rights reserved."

from collections.abc import Callable

import numpy as np
import numpy.typing

from EV_sim.ev import EV
from EV_sim.extern_conditions import ExternalConditions
from EV_sim.drivecycles import DriveCycle
from EV_sim.utils.constants import PhysicsConstants
from EV_sim.sol import Solution
from EV_sim.utils.timer import sol_timer


class VehicleDynamics:
    """
    VehicleDynamics simulates the demanded power and current from the batter pack.
    """

    def __init__(self, ev_obj: EV, drive_cycle_obj: DriveCycle, external_condition_obj: ExternalConditions) -> None:
        """
        VehicleDynamics class constructor.
        :param ev_obj: (EV) EV class object that contains vehicle parameters.
        :param drive_cycle_obj: (DriveCycle) Drive cycle class object that contains all relevant drive cycle parameters.
        :param external_condition_obj: (ExternalConditions) ExternalConditions class object that contains all relevant
        external condition parameters.
        """
        if isinstance(ev_obj, EV):
            self.EV = ev_obj
        else:
            raise TypeError("ev_obj needs to be a EV object.")

        if isinstance(drive_cycle_obj, DriveCycle):
            self.DriveCycle = drive_cycle_obj
        else:
            raise TypeError("DriveCycle_obj needs to be DriveCycle object.")

        if isinstance(external_condition_obj, ExternalConditions):
            self.ExtCond = external_condition_obj
        else:
            raise TypeError("external_condition_onj needs to be External condition object.")

        if isinstance(self.ExtCond.road_grade_angle, np.ndarray):
            if len(self.ExtCond.road_grade_angle) != len(self.DriveCycle.t):
                raise ValueError("The lengths of external condition's road grade and drive cycle's time array do not "
                                 "match.")

    @property
    def des_speed(self) -> numpy.typing.ArrayLike:
        """
        Desired vehicle speed in m/s.
        :return: (np.ndarray) Array of desired speed, m/s
        """
        return np.minimum(self.DriveCycle.speed_kmph, self.EV.max_speed) / 3.6

    @staticmethod
    def desired_acc(desired_speed: float, prev_speed: float, current_time: float, prev_time: float) -> float:
        """
        Calculates and returns the desired acceleration, m/s^2.
        :param desired_speed: (float) desired speed, m/s
        :param prev_speed: (float) speed at the previous time step, m/s
        :param current_time: (float): time at the current time step, s
        :param prev_time: (float): time at the previous time step, s
        :return: (float) desired acceleration, m/s^2
        """
        return (desired_speed - prev_speed) / (current_time - prev_time)

    @staticmethod
    def desired_acc_F(equivalent_mass: float, desired_acc: float) -> float:
        """
        Calculates the desired accelerating force in N.
        :param equivalent_mass: (float) Equivalent vehicle mass, kg
        :param desired_acc: (float) acceleration, m/s^2
        :return: (float) desired acceleration
        """
        return equivalent_mass * desired_acc

    @staticmethod
    def aero_F(air_density: float, aero_frontal_area: float, C_d: float, prev_speed: float) -> float:
        """
        Calculates the aerodynamic drag in N.
        :param air_density: External air density, kg/m^3
        :param aero_frontal_area: Vehicle frontal area, m^2
        :param C_d: Drag coefficient, unit-;ess
        :param prev_speed: Speed at the previous time step, m/s
        :return: (float) aerodynamic drag, N
        """
        return 0.5 * air_density * aero_frontal_area * C_d * (prev_speed ** 2)

    @staticmethod
    def roll_grade_F(max_veh_mass: float, gravity_acc: float, grade_angle: float) -> float:
        """
        Calculates the rolling grade force.
        :param C_r: rolling coefficient, unit-less
        :param max_veh_mass: max. vehicle mass, kg
        :param gravity_acc: acceleration of gravity, 9.81 g/m^2
        :param grade_angle: grade_angle, rad
        :return:  (float) rolling grade force, N
        """
        return max_veh_mass * gravity_acc * np.sin(grade_angle)

    @staticmethod
    def demand_torque(des_acc_F: float, aero_F: float, roll_grade_F: float, road_F: float, wheel_radius: float,
                      gear_ratio: float) -> float:
        return (des_acc_F + aero_F + roll_grade_F + road_F) * wheel_radius / gear_ratio

    def init_cond(self):
        """
        Simulation initial conditions
        :return: (float) Returns the initial conditions of the relevant simulation variables.
        """
        prev_speed = 0
        prev_motor_speed = 0
        prev_distance = 0
        prev_SOC = 0
        prev_time = 2 * self.DriveCycle.t[0] - self.DriveCycle.t[1]
        return prev_speed, prev_motor_speed, prev_distance, prev_SOC, prev_time

    def create_init_arrays(self) -> Solution:
        """
        Create numpy arrays with zero elements of the desired sizes for all the simulation results. These simulation
        results are stored in the instance 'sol' of the Solution class.
        :return: (tuple) Solution object whose attributes are numpy arrays with zero elements (except for it's t (time)
        attribute).
        """
        sol = Solution(veh_alias=self.EV.alias_name, t=self.DriveCycle.t)
        return sol

    @staticmethod
    def simulate_over_all_timesteps(func) -> Callable[[], Solution]:
        """
        Acts as a decorator function, whose wrapper function defines the initial conditions and performs simulation
        iterations over all time steps.
        :param func: (function type) simulation function
        """

        @sol_timer
        def initialize_and_iterations(self) -> Solution:
            prev_speed, prev_motor_speed, prev_distance, prev_SOC, prev_time = self.init_cond()  # initialization
            sol = self.create_init_arrays()  # create arrays for results and calculations
            # Run the simulation.
            for k in range(len(self.DriveCycle.t)):  # k represents time index.
                func(self, sol, k, prev_time, prev_speed, prev_motor_speed, prev_distance, prev_SOC)
                # update relevant variables below
                prev_time = self.DriveCycle.t[k]
                prev_speed = sol.actual_speed[k]
                prev_motor_speed = sol.motor_speed[k]
                prev_distance = sol.distance[k]
                prev_SOC = sol.battery_SOC[k]
            return sol

        return initialize_and_iterations

    @simulate_over_all_timesteps
    def simulate(self, sol: Solution, k: int, prev_time: float, prev_speed: float, prev_motor_speed: float,
                 prev_distance: float, prev_SOC: float) -> None:
        """
        Performs vehicle dynamics simulation at a specific time step, k. It updates the Solution instance attributes
        at this time step, k.
        :param sol: Solution object that contains the all the simulation results in a arrays.
        :param k: time step
        :param prev_time: time at the previous time step
        :param prev_speed: speed at the previous time step
        :param prev_motor_speed: motor speed at the previous time step.
        :param prev_distance: distance at the previous time step.
        :param prev_SOC: SOC at the previous time step.
        :return: (None)
        """
        sol.des_acc[k] = VehicleDynamics.desired_acc(desired_speed=self.des_speed[k], prev_speed=prev_speed,
                                                     current_time=self.DriveCycle.t[k], prev_time=prev_time)
        sol.des_acc_F[k] = VehicleDynamics.desired_acc_F(equivalent_mass=self.EV.equiv_mass, desired_acc=sol.des_acc[k])
        sol.aero_F[k] = VehicleDynamics.aero_F(self.ExtCond.rho, self.EV.A_front, self.EV.C_d, prev_speed)
        sol.roll_grade_F[k] = VehicleDynamics.roll_grade_F(max_veh_mass=self.EV.max_mass,
                                                           gravity_acc=PhysicsConstants.g,
                                                           grade_angle=self.ExtCond.road_grade_angle)
        if np.abs(prev_speed) > 0:
            sol.roll_grade_F[k] = sol.roll_grade_F[k] + self.EV.C_r * self.EV.max_mass * PhysicsConstants.g
        sol.demand_torque[k] = VehicleDynamics.demand_torque(des_acc_F=sol.des_acc_F[k], aero_F=sol.aero_F[k],
                                                             roll_grade_F=sol.roll_grade_F[k],
                                                             road_F=self.ExtCond.road_force,
                                                             wheel_radius=self.EV.drive_train.wheel.r,
                                                             gear_ratio=self.EV.drive_train.gear_box.N)

        # The remaining calculations leads to actual speed
        # First check if demand torque is limited by the motor characteristics and calculate the max. torque and
        # limit torque
        if prev_motor_speed < self.EV.motor.RPM_r:
            sol.max_torque[k] = self.EV.motor.L_max
        else:
            sol.max_torque[k] = self.EV.motor.L_max * self.EV.motor.RPM_r / prev_motor_speed

        sol.limit_regen[k] = np.minimum(sol.max_torque[k], self.EV.drive_train.frac_regen_torque * self.EV.motor.L_max)
        sol.limit_torque[k] = np.minimum(sol.demand_torque[k], sol.max_torque[k])
        if sol.limit_torque[k] > 0:
            sol.motor_torque[k] = sol.limit_torque[k]
        else:
            sol.motor_torque[k] = np.maximum(-sol.limit_regen[k], sol.limit_torque[k])

        # Now calculate the actual accelerations and speeds. Finally, the distance is calculated
        sol.actual_acc_F[k] = sol.limit_torque[k] * self.EV.drive_train.gear_box.N / self.EV.drive_train.wheel.r - \
                              sol.aero_F[k] - sol.roll_grade_F[k] - self.ExtCond.road_force
        sol.actual_acc[k] = sol.actual_acc_F[k] / self.EV.equiv_mass
        sol.motor_speed[k] = np.minimum(self.EV.motor.RPM_max, self.EV.drive_train.gear_box.N * (
                prev_speed + sol.actual_acc[k] * (self.DriveCycle.t[k] - prev_time)) * 60 / (
                                                2 * np.pi * self.EV.drive_train.wheel.r))
        sol.actual_speed[k] = sol.motor_speed[k] * 2 * np.pi * self.EV.drive_train.wheel.r / (
                60 * self.EV.drive_train.gear_box.N)
        sol.actual_speed_kmph[k] = sol.actual_speed[k] * 3600 / 1000
        sol.distance[k] = prev_distance + ((sol.actual_speed[k] + prev_speed) / 2) * (self.DriveCycle.t[k] -
                                                                                      prev_time) / 1000

        # Finally, calculates the battery power, current demanded
        if sol.limit_torque[k] > 0:
            sol.demand_power[k] = sol.limit_torque[k]
        else:
            sol.demand_power[k] = np.maximum(sol.limit_torque[k], -sol.limit_regen[k])
        sol.demand_power[k] = (sol.demand_power[k] * 2 * np.pi) * (prev_motor_speed + sol.motor_speed[k]) / (2 * 60000)
        sol.limit_power[k] = np.maximum(-self.EV.motor.P_max, np.minimum(self.EV.motor.P_max, sol.demand_power[k]))
        sol.battery_demand[k] = self.EV.overhead_power / 1000
        if sol.limit_power[k] > 0:
            sol.battery_demand[k] = sol.battery_demand[k] + sol.limit_power[k] / self.EV.drive_train.eff
        else:
            sol.battery_demand[k] = sol.battery_demand[k] + sol.limit_power[k] * self.EV.drive_train.eff
        sol.current[k] = sol.battery_demand[k] * 1000 / self.EV.pack.pack_V_nom
        sol.cell_current[k] = sol.current[k] / self.EV.pack.Np
        sol.battery_SOC[k] = prev_SOC - sol.current[k] * (self.DriveCycle.t[k] - prev_time)

    def __repr__(self):
        return f"VehicleDynamics({self.EV}, {self.DriveCycle}, {self.ExtCond})"

    def __str__(self):
        return f"Vehicle Alias: {self.EV.alias_name} driving along {self.DriveCycle.drive_cycle_name}."
