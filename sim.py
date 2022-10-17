import numpy as np

from setup_vehicle import Vehicle
from setup_drivecycles import Drive_cycle


class Sim:
    def __init__(self, vehicle, drive_cycle, sim_params):
        # check for correct input types
        if not (isinstance(vehicle, Vehicle)):
            raise TypeError("vehicle needs to be an instance of Class:Vehicle")
        if not (isinstance(drive_cycle, Drive_cycle)):
            raise TypeError("drive_cycle needs to be an instance if Class:Drive_cycle")
        if not (isinstance(sim_params, dict)):
            raise TypeError("sim_params needs to be right instance of the dict object.")
        self.vehicle = vehicle
        self.drive_cycle = drive_cycle
        self.rho = sim_params["air_density [kg/m3]"]
        self.grade = sim_params["road grade [in rad]"]

    @property
    def des_speed(self):
        return np.minimum(self.drive_cycle.speed_mps, self.vehicle.veh_max_speed * 1000 / 3600)

    @staticmethod
    def desired_acc(desired_speed, actual_speed, t_curr, t_prev):
        return (desired_speed - actual_speed)/(t_curr - t_prev)

    @staticmethod
    def desired_acc_F(equivalent_mass, desired_acc):
        return equivalent_mass * desired_acc

    @staticmethod
    def aero_F(air_density, aero_frontal_area, C_d, prev_speed):
        return 0.5 * air_density * aero_frontal_area * C_d * (prev_speed**2)

    @staticmethod
    def rolling_F(rolling_fric_coeff, max_veh_mass, gravity_acc, grade):
        return rolling_fric_coeff * max_veh_mass * gravity_acc * np.sin(grade)

    @staticmethod
    def demand_torque(des_acc_F, aero_F, roll_grade_F, road_F, wheel_radius, gear_ratio):
        return (des_acc_F + aero_F + roll_grade_F + road_F) * wheel_radius / gear_ratio

    def simulate(self):
        # intialization
        prev_speed = 0
        prev_motor_speed = 0
        prev_distance = 0
        prev_SOC = 0
        prev_time = 2 * self.drive_cycle.time_s[0] - self.drive_cycle.time_s[1]

        # create arrays for results and calculations
        des_acc = np.zeros(len(self.drive_cycle.time_s))
        des_acc_F = np.zeros(len(self.drive_cycle.time_s))
        aero_F = np.zeros(len(self.drive_cycle.time_s))
        roll_grade_F = np.zeros(len(self.drive_cycle.time_s))
        demand_torque = np.zeros(len(self.drive_cycle.time_s))
        max_torque = np.zeros(len(self.drive_cycle.time_s))
        limit_regen = np.zeros(len(self.drive_cycle.time_s))
        limit_torque = np.zeros(len(self.drive_cycle.time_s))
        motor_torque = np.zeros(len(self.drive_cycle.time_s))
        actual_acc_F = np.zeros(len(self.drive_cycle.time_s))
        actual_acc = np.zeros(len(self.drive_cycle.time_s))
        motor_speed = np.zeros(len(self.drive_cycle.time_s))
        actual_speed = np.zeros(len(self.drive_cycle.time_s))
        actual_speed_kmph = np.zeros(len(self.drive_cycle.time_s))
        distance = np.zeros(len(self.drive_cycle.time_s))
        motor_power = np.zeros(len(self.drive_cycle.time_s))
        limit_power = np.zeros(len(self.drive_cycle.time_s))
        battery_demand = np.zeros(len(self.drive_cycle.time_s))
        current = np.zeros(len(self.drive_cycle.time_s))
        battery_SOC = np.zeros(len(self.drive_cycle.time_s))

        for k in range(len(self.drive_cycle.time_s)):
            des_acc[k] = Sim.desired_acc(self.des_speed[k], prev_speed, self.drive_cycle.time_s[k], prev_time)
            des_acc_F[k] = Sim.desired_acc_F(self.vehicle.veh_equiv_mass, des_acc[k])
            aero_F[k] = Sim.aero_F(self.rho, self.vehicle.frontal_area, self.vehicle.C_d, prev_speed)
            roll_grade_F[k] = Sim.rolling_F(1, self.vehicle.veh_max_mass, 9.81, self.grade)
            if np.abs(prev_speed) > 0:
                roll_grade_F[k] = roll_grade_F[k] + Sim.rolling_F(self.vehicle.roll_coeff, self.vehicle.veh_max_mass, 9.81, np.pi/2)
            # demand_torque[k] = (des_acc_F[k] + aero_F[k] + roll_grade_F[k] + self.vehicle.road_force) * \
            #                    self.vehicle.wheel_radius / self.vehicle.gear_ratio
            demand_torque[k] = Sim.demand_torque(des_acc_F[k], aero_F[k], roll_grade_F[k], self.vehicle.road_force, self.vehicle.wheel_radius, self.vehicle.gear_ratio)

            # demand torque is limited by the motor characteristics:
            if prev_motor_speed < self.vehicle.RPM_rated:
                max_torque[k] = self.vehicle.Lmax
            else:
                max_torque[k] = self.vehicle.Lmax * self.vehicle.RPM_rated / prev_motor_speed
            limit_regen[k] = np.minimum(max_torque[k], self.vehicle.frac_regen_torque * self.vehicle.Lmax)
            limit_torque[k] = np.minimum(demand_torque[k], max_torque[k])
            if limit_torque[k] > 0:
                motor_torque[k] = limit_torque[k]
            else:
                motor_torque[k] = np.maximum(-limit_regen[k], limit_torque[k])

            # calculate the actual values
            actual_acc_F[k] = limit_torque[k] * self.vehicle.gear_ratio / self.vehicle.wheel_radius - aero_F[k] - \
                            roll_grade_F[k] - self.vehicle.road_force
            actual_acc[k] = actual_acc_F[k] / self.vehicle.veh_equiv_mass
            motor_speed[k] = np.minimum(self.vehicle.RPM_max, self.vehicle.gear_ratio * (prev_speed + actual_acc[k] * (self.drive_cycle.time_s[k] - prev_time)) * 60 / (2 * np.pi * self.vehicle.wheel_radius))
            actual_speed[k] = motor_speed[k] * 2 * np.pi * self.vehicle.wheel_radius / (60 * self.vehicle.gear_ratio)
            actual_speed_kmph[k] = actual_speed[k] * 3600/1000
            distance[k] = prev_distance + ((actual_speed[k] + prev_speed)/2) * (self.drive_cycle.time_s[k] - prev_time)/1000

            # calculates the battery power, current demanded
            if limit_torque[k] > 0:
                motor_power[k] = limit_torque[k]
            else:
                motor_power[k] = np.minimum(limit_torque[k], -limit_regen[k])
            motor_power[k] = (motor_power[k] * 2 * np.pi / 60000) * (prev_motor_speed + motor_speed[k])/2
            limit_power[k] = np.maximum(-self.vehicle.motor_max_power, np.minimum(self.vehicle.motor_max_power, motor_power[k]))
            battery_demand[k] = self.vehicle.overhead_power / 1000
            if limit_power[k] > 0:
                battery_demand[k] = battery_demand[k] + limit_power[k] / self.vehicle.dt_eff
            else:
                battery_demand[k] = battery_demand[k] + limit_power[k] * self.vehicle.dt_eff
            current[k] = battery_demand[k] * 1000 / self.vehicle.pack_V_nom
            battery_SOC[k] = prev_SOC - current[k] * (self.drive_cycle.time_s[k] - prev_time)

            # update relevant variables
            prev_time = self.drive_cycle.time_s[k]
            prev_speed = actual_speed[k]
            prev_motor_speed = motor_speed[k]
            prev_distance = distance[k]
            prev_SOC = battery_SOC[k]

        return des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque, limit_regen, limit_torque, \
               motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed, actual_speed_kmph, distance, \
               motor_power, limit_power, battery_demand, current, battery_SOC
