#  Copyright (c) 2023. Moin Ahmed. All Rights Reserved.

from typing import Optional, Union
import numpy.typing as npt

import EV_sim
from EV_sim.custom_exceptions import *


class InputSimVariables:
    """
    Stores the instances of simulation variables. Furthermore, it contains methods for instance retrieval and update.
    """
    def __init__(self):
        self.ev_obj_instances = []
        self.create_EV_instance()
        self.dc_obj = EV_sim.DriveCycle(drive_cycle_name=None)  # stores the DriveCycle object and initializes with a
        # the first drive cycle text file in the data/drive_cycles folder
        self.ext_cond_obj = EV_sim.ExternalConditions(rho=None, road_grade=None, road_force=None)
        self.sol = None

    def create_EV_instance(self):
        """
        creates an empty EV instance and updates to EV instances list
        :return: None
        """
        self.ev_obj_instances.append(EV_sim.EV())

    def update_EV_instance(self, instance_index: int, alias_name: float) -> None:
        """
        Updates an EV instance in the list (EV instance corresponding to the instance_index) with the input EV alias
        name.
        :param instance_index: (int) index in the EV instance list
        :param alias_name: (str) EV instance name
        :return: (None)
        """
        if self.ev_obj_instances:
            if (instance_index < len(self.ev_obj_instances)):
                self.ev_obj_instances[instance_index] = EV_sim.EVFromDatabase(alias_name=alias_name)
            else:
                raise ValueError('Inputted instance_index exceeds the length of the ev_obj_instances list')

    def update_drivecycle_instance(self, drive_cycle_name: str) -> None:
        """
        Updates the drive cycle instance with the drive cycle name.
        :param drive_cycle_name: (str) drive cycle name
        :return: (None)
        """
        if isinstance(drive_cycle_name, str):
            self.dc_obj = EV_sim.DriveCycle(drive_cycle_name=drive_cycle_name)
        else:
            raise UndefinedDriveCycleError

    def update_ext_cond_instance(self, rho:float, road_grade: Union[Optional[float], npt.ArrayLike], road_force: float):
        """
        Updates the external condition instance with the external conditions parameters.
        :param rho: external air density, kg / m^3
        :param road_grade: represents the amount of road rise or drop. For e.g., a road grade of 5 % means that the
        road will rise 5 ft over the next 100 ft.
        :param: (float) constant road force input by the EV driver, N
        :return: (None)
        """
        self.ext_cond_obj = EV_sim.ExternalConditions(rho=rho, road_grade=road_grade, road_force=road_force)

    def sim(self):
        if self.ev_obj_instances[0].alias_name == None:
            raise UndefinedEVError
        if self.dc_obj.drive_cycle_name == None:
            raise UndefinedDriveCycleError
        if self.ext_cond_obj.rho == None:
            raise UndefinedRhoError
        if self.ext_cond_obj.road_force==None:
            raise UndefinedRoadForce
        model = EV_sim.VehicleDynamics(ev_obj=self.ev_obj_instances[0], drive_cycle_obj=self.dc_obj,
                                       external_condition_obj=self.ext_cond_obj)
        self.sol = model.simulate()
        return model.simulate()

    def update_rho(self, rho):
        if isinstance(rho, float):
            self.ext_cond_obj.rho = rho
        else:
            raise UndefinedRhoError

    def update_road_grade(self, road_grade):
        if isinstance(road_grade, float):
            self.ext_cond_obj.road_grade = road_grade
        else:
            raise TypeError("Road grade needs to be a float.")

    def update_road_force(self, road_force):
        if isinstance(road_force, float):
            self.ext_cond_obj.road_force = road_force
        else:
            raise TypeError("road force needs to be a float.")


# # protype testing
# a = InputSimVariables()
# print(a.ev_obj_instances)
# a.update_EV_instance(0, 'Volt_2017')
# print(a.ev_obj_instances)
