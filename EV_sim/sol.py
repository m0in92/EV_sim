import numpy as np
import matplotlib.pyplot as plt


class Solution:
    """
    Class object that stores the simulation results from the model. Furthermore, it contains methods to plot the
    results.
    """

    def __init__(self, veh_alias: str, t, des_acc, des_acc_F, aero_F, roll_grade_F, demand_torque, max_torque,
                 limit_regen, limit_torque, motor_torque, actual_acc_F, actual_acc, motor_speed, actual_speed,
                 actual_speed_kmph, distance, demand_power, limit_power, battery_demand, current, battery_SOC):
        self.veh_alias = veh_alias  # vehicle alias
        self.t = t  # time array, s
        self.des_acc = des_acc
        self.des_acc_F = des_acc_F
        self.aero_F = aero_F
        self.roll_grade_F = roll_grade_F
        self.demand_torque = demand_torque
        self.max_torque = max_torque
        self.limit_regen = limit_regen
        self.limit_torque = limit_torque
        self.motor_torque = motor_torque
        self.actual_acc_F = actual_acc_F
        self.actual_acc = actual_acc
        self.motor_speed = motor_speed
        self.actual_speed = actual_speed
        self.actual_speed_kmph = actual_speed_kmph
        self.distance = distance
        self.demand_power = demand_power
        self.limit_power = limit_power
        self.battery_demand = battery_demand
        self.current = current
        self.battery_SOC = battery_SOC

    def plot_battery_demand(self):
        """
        Displays a simple plot of the battery demnaded power vs. time
        :param t_array: time array, s
        :param veh_alias_name: vehicle alias name
        :return: (plt.figure) figure object
        """
        fig = plt.figure()
        ax1 = fig.add_subplot()
        ax1.plot(self.t / 60, self.demand_power)  # the time will be in minutes
        ax1.set_title(f"{self.veh_alias}")
        ax1.set_xlabel('Time [min]')
        ax1.set_ylabel('Battery power demand [kW]')
        return fig

    def plot(self):
        """
        Displays a simple plot of battery demand power and current.
        :param t_array: time array, s
        :param veh_alias_name: vehicle alias name
        :return: None
        """
        fig = plt.figure()

        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(self.t / 60, self.demand_power)  # the time will be in minutes
        ax1.set_title(f"{self.veh_alias}")
        ax1.set_xlabel('Time [min]')
        ax1.set_ylabel('Battery power demand [kW]')

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(self.t / 60, self.current)  # the time will be in minutes
        ax2.set_xlabel('Time [min]')
        ax2.set_ylabel('Battery Current [A]')

        plt.tight_layout()
        plt.show()
