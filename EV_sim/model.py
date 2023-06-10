import numpy as np
import numpy.typing

from EV_sim.ev import EV
from EV_sim.extern_conditions import ExternalConditions
from EV_sim.drivecycles import DriveCycle
from EV_sim.constants import PhysicsConstants
from EV_sim.sol import Solution
from EV_sim.utils.timer import sol_timer


class VehicleDynamics:
    """
    VehicleDynamics simulates the demanded power and current from the batter pack.
    """
    def __init__(self, ev_obj: EV, drive_cycle_obj: DriveCycle, external_condition_obj: ExternalConditions):
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
    def desired_acc(desired_speed: float, prev_speed: float, current_time: float, prev_time:float) -> float:
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
        return 0.5 * air_density * aero_frontal_area * C_d * (prev_speed**2)

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

    def create_init_arrays(self):
        """
        Create zeros numpy arrays of the desired sizes for all the simulation results
        :return: (tuple) Tuple of zeros numpy arrays for the storage of results.
        """
        des_acc = np.zeros(len(self.DriveCycle.t))
        des_acc_F = np.zeros(len(self.DriveCycle.t))
        aero_F = np.zeros(len(self.DriveCycle.t))
        roll_grade_F = np.zeros(len(self.DriveCycle.t))
        demand_torque = np.zeros(len(self.DriveCycle.t))
        max_torque = np.zeros(len(self.DriveCycle.t))
        limit_regen = np.zeros(len(self.DriveCycle.t))
        limit_torque = np.zeros(len(self.DriveCycle.t))
        motor_torque = np.zeros(len(self.DriveCycle.t))
        actual_acc_F = np.zeros(len(self.DriveCycle.t))
        actual_acc = np.zeros(len(self.DriveCycle.t))
        motor_speed = np.zeros(len(self.DriveCycle.t))
        actual_speed = np.zeros(len(self.DriveCycle.t)) # actual speed, m/s
        actual_speed_kmph = np.zeros(len(self.DriveCycle.t)) # actual speed, km/h
        distance = np.zeros(len(self.DriveCycle.t))
        demand_power = np.zeros(len(self.DriveCycle.t))
        limit_power = np.zeros(len(self.DriveCycle.t))
        battery_demand = np.zeros(len(self.DriveCycle.t))
        current = np.zeros(len(self.DriveCycle.t))
        battery_SOC = np.zeros(len(self.DriveCycle.t))

        return des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque, limit_regen, limit_torque, \
               motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed, actual_speed_kmph, distance, \
               demand_power, limit_power, battery_demand, current, battery_SOC

    def simulate_k(self, des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque, limit_regen, limit_torque,
                   motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed, actual_speed_kmph, distance,
                   demand_power, limit_power, battery_demand, current, battery_SOC, k, prev_time, prev_speed,
                   prev_motor_speed, prev_distance, prev_SOC):
        """
        Vehicle dynamics simulation at a time step, k
        :param des_acc:
        :param des_acc_F:
        :param aero_F:
        :param roll_grade_F:
        :param demand_torque:
        :param max_torque:
        :param limit_regen:
        :param limit_torque:
        :param motor_torque:
        :param actual_acc_F:
        :param actual_acc:
        :param motor_speed:
        :param actual_speed:
        :param actual_speed_kmph:
        :param distance:
        :param demand_power:
        :param limit_power:
        :param battery_demand:
        :param current:
        :param battery_SOC:
        :param k:
        :param prev_time:
        :param prev_speed:
        :param prev_motor_speed:
        :param prev_distance:
        :param prev_SOC:
        :return:
        """
        des_acc[k] = VehicleDynamics.desired_acc(desired_speed=self.des_speed[k], prev_speed=prev_speed,
                                                 current_time=self.DriveCycle.t[k], prev_time=prev_time)
        des_acc_F[k] = VehicleDynamics.desired_acc_F(equivalent_mass=self.EV.equiv_mass, desired_acc=des_acc[k])
        aero_F[k] = VehicleDynamics.aero_F(self.ExtCond.rho, self.EV.A_front, self.EV.C_d, prev_speed)
        roll_grade_F[k] = VehicleDynamics.roll_grade_F(max_veh_mass=self.EV.max_mass,
                                                       gravity_acc=PhysicsConstants.g,
                                                       grade_angle=self.ExtCond.road_grade_angle)
        if np.abs(prev_speed) > 0:
            roll_grade_F[k] = roll_grade_F[k] + self.EV.C_r * self.EV.max_mass * PhysicsConstants.g
        demand_torque[k] = VehicleDynamics.demand_torque(des_acc_F=des_acc_F[k], aero_F=aero_F[k],
                                                         roll_grade_F=roll_grade_F[k],
                                                         road_F=self.ExtCond.road_force,
                                                         wheel_radius=self.EV.drive_train.wheel.r,
                                                         gear_ratio=self.EV.drive_train.gear_box.N)

        # The remaining calculations leads to actual speed
        # First check if demand torque is limited by the motor characteristics and calculate the max. torque and
        # limit torque
        if prev_motor_speed < self.EV.motor.RPM_r:
            max_torque[k] = self.EV.motor.L_max
        else:
            max_torque[k] = self.EV.motor.L_max * self.EV.motor.RPM_r / prev_motor_speed

        limit_regen[k] = np.minimum(max_torque[k], self.EV.drive_train.frac_regen_torque * self.EV.motor.L_max)
        limit_torque[k] = np.minimum(demand_torque[k], max_torque[k])
        if limit_torque[k] > 0:
            motor_torque[k] = limit_torque[k]
        else:
            motor_torque[k] = np.maximum(-limit_regen[k], limit_torque[k])

        ## Now calculate the actual accelerations and speeds. Finally the distance is calculated
        actual_acc_F[k] = limit_torque[k] * self.EV.drive_train.gear_box.N / self.EV.drive_train.wheel.r - \
                          aero_F[k] - roll_grade_F[k] - self.ExtCond.road_force
        actual_acc[k] = actual_acc_F[k] / self.EV.equiv_mass
        motor_speed[k] = np.minimum(self.EV.motor.RPM_max, self.EV.drive_train.gear_box.N * (
                prev_speed + actual_acc[k] * (self.DriveCycle.t[k] - prev_time)) * 60 / (
                                            2 * np.pi * self.EV.drive_train.wheel.r))
        actual_speed[k] = motor_speed[k] * 2 * np.pi * self.EV.drive_train.wheel.r / (
                    60 * self.EV.drive_train.gear_box.N)
        actual_speed_kmph[k] = actual_speed[k] * 3600 / 1000
        distance[k] = prev_distance + ((actual_speed[k] + prev_speed) / 2) * (self.DriveCycle.t[k] - prev_time) / 1000

        # Finally, calculates the battery power, current demanded
        if limit_torque[k] > 0:
            demand_power[k] = limit_torque[k]
        else:
            demand_power[k] = np.maximum(limit_torque[k], -limit_regen[k])
        demand_power[k] = (demand_power[k] * 2 * np.pi) * (prev_motor_speed + motor_speed[k]) / (2 * 60000)
        limit_power[k] = np.maximum(-self.EV.motor.P_max, np.minimum(self.EV.motor.P_max, demand_power[k]))
        battery_demand[k] = self.EV.overhead_power / 1000
        if limit_power[k] > 0:
            battery_demand[k] = battery_demand[k] + limit_power[k] / self.EV.drive_train.eff
        else:
            battery_demand[k] = battery_demand[k] + limit_power[k] * self.EV.drive_train.eff
        current[k] = battery_demand[k] * 1000 / self.EV.pack.pack_V_nom
        battery_SOC[k] = prev_SOC - current[k] * (self.DriveCycle.t[k] - prev_time)

    @sol_timer
    def simulate(self):
        # initialization
        prev_speed, prev_motor_speed, prev_distance, prev_SOC, prev_time = self.init_cond()

        # create arrays for results and calculations
        des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque, limit_regen, limit_torque, \
        motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed, actual_speed_kmph, distance, \
        demand_power, limit_power, battery_demand, current, battery_SOC = self.create_init_arrays()

        # Run the simulation.
        for k in range(len(self.DriveCycle.t)): # k represents time index.

            self.simulate_k(des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque, limit_regen,
                            limit_torque, motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed,
                            actual_speed_kmph, distance, demand_power, limit_power, battery_demand, current,
                            battery_SOC, k, prev_time, prev_speed, prev_motor_speed, prev_distance, prev_SOC)

            # update relevant variables
            prev_time = self.DriveCycle.t[k]
            prev_speed = actual_speed[k]
            prev_motor_speed = motor_speed[k]
            prev_distance = distance[k]
            prev_SOC = battery_SOC[k]

        return Solution(self.EV.alias_name, self.DriveCycle.t, des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque,
                        max_torque, limit_regen, limit_torque, motor_torque, actual_acc_F, actual_acc, motor_speed,
                        actual_speed, actual_speed_kmph, distance, demand_power, limit_power, battery_demand, current,
                        battery_SOC)

    def __repr__(self):
        return f"VehicleDynamics({self.EV}, {self.DriveCycle}, {self.ExtCond})"

    def __str__(self):
        return f"Vehicle Alias: {self.EV.alias_name} driving along {self.DriveCycle.drive_cycle_name}."


