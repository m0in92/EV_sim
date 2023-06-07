from dataclasses import dataclass
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
    des_acc: Optional[npt.ArrayLike]
    des_acc_F: Optional[npt.ArrayLike]
    aero_F: Optional[npt.ArrayLike]
    roll_grade_F: Optional[npt.ArrayLike]
    demand_torque: Optional[npt.ArrayLike]
    max_torque: Optional[npt.ArrayLike]
    limit_regen: Optional[npt.ArrayLike]
    limit_torque: Optional[npt.ArrayLike]
    motor_torque: Optional[npt.ArrayLike]
    actual_acc_F: Optional[npt.ArrayLike]
    actual_acc: Optional[npt.ArrayLike]
    motor_speed: Optional[npt.ArrayLike]
    actual_speed: Optional[npt.ArrayLike]
    actual_speed_kmph: Optional[npt.ArrayLike]
    distance: Optional[npt.ArrayLike]
    demand_power: Optional[npt.ArrayLike]
    limit_power: Optional[npt.ArrayLike]
    battery_demand: Optional[npt.ArrayLike]
    current: Optional[npt.ArrayLike]
    battery_SOC: Optional[npt.ArrayLike]

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
