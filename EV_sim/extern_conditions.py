from typing import Optional, overload, Union

import numpy as np
import numpy.typing as npt


class ExternalConditions:
    """
    ExternalConditions stores the density, road grade and road force parameters.
    """
    @overload
    def __init__(self, rho: None, road_grade: None, road_force: None):
        ...

    @overload
    def __init__(self, rho:float, road_grade:float, road_force:float):
        ...

    def __init__(self, rho: Optional[float], road_grade: Union[Optional[float], npt.ArrayLike],
                 road_force: Optional[float] = 0.0):
        """
        ExternalConditions constructor
        :param rho: external air density, kg / m^3
        :param road_grade: represents the amount of road rise or drop. For e.g., a road grade of 5 % means that the
        road will rise 5 ft over the next 100 ft.
        :param: (float) constant road force input by the EV driver, N
        """
        if isinstance(rho, float) or (rho is None):
            self.rho = rho
        else:
            raise TypeError("External air density needs to be a float.")

        if isinstance(road_grade, float) or isinstance(road_grade, np.ndarray):
            self.road_grade = road_grade # road grade, %
            self.road_grade_angle = np.arctan(road_grade / 100)  # road grade angle, rad
        elif road_grade is None:
            self.road_grade = None
        else:
            raise TypeError("External road grade needs to be a float or a numpy array.")
        # self.road_grade_angle = np.arctan(road_grade / 100)  # road grade angle, rad

        if isinstance(road_force, float) or (road_force is None):
            self.road_force = road_force
        else:
            raise TypeError("Road force needs to be a float.")

    def __repr__(self):
        return f"ExternalConditions({self.rho}, {self.road_grade}, {self.road_force})"

    def __str__(self):
        return f"air_pressure: {self.rho}, road_grade:{self.road_grade}, road_force: {self.road_force}"
