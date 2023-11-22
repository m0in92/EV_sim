"""
This modules contains the classes and functionailities for storing the simulation results.
"""

__all__ = ['Solution']

__authors__ = "Moin Ahmed"
__copyright__ = 'Copyright 2023 by EV_sim. All rights reserved.'

from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
import numpy.typing as npt
from typing import Optional


@dataclass
class Solution:
    """
    Class object that stores the simulation results from the model. Furthermore, it contains methods to plot the
    results.
    """
    veh_alias: Optional[str]
    t: Optional[npt.ArrayLike]

    def __post_init__(self):
        if isinstance(self.t, np.ndarray):
            self.des_acc = np.zeros(len(self.t))
            self.des_acc_F = np.zeros(len(self.t))
            self.aero_F = np.zeros(len(self.t))
            self.roll_grade_F = np.zeros(len(self.t))
            self.demand_torque = np.zeros(len(self.t))
            self.max_torque = np.zeros(len(self.t))
            self.limit_regen = np.zeros(len(self.t))
            self.limit_torque = np.zeros(len(self.t))
            self.motor_torque = np.zeros(len(self.t))
            self.actual_acc_F = np.zeros(len(self.t))
            self.actual_acc = np.zeros(len(self.t))
            self.motor_speed = np.zeros(len(self.t))
            self.actual_speed = np.zeros(len(self.t))  # actual speed, m/s
            self.actual_speed_kmph = np.zeros(len(self.t))  # actual speed, km/h
            self.distance = np.zeros(len(self.t))
            self.demand_power = np.zeros(len(self.t))
            self.limit_power = np.zeros(len(self.t))
            self.battery_demand = np.zeros(len(self.t))
            self.current = np.zeros(len(self.t))
            self.cell_current = np.zeros(len(self.t))
            self.battery_SOC = np.zeros(len(self.t))

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
