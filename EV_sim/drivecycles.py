import os
import typing
from typing import overload

import pandas as pd
import matplotlib.pyplot as plt

from EV_sim.config import definations


class DriveCycle:
    """
    DriveCycle class searches for and stores arrays of time and desired speed information.
    """

    @overload
    def __int__(self, drive_cycle_name: str) -> None:
        ...

    @overload
    def __init(self, drive_cycle_name: None) -> None:
        ...

    def __init__(self, drive_cycle_name: typing.Optional[str],
                 folder_dir: str = os.path.join(definations.ROOT_DIR, "data", "drive_cycles")):
        """
        DriveCycle constructor
        :param drive_cycle_name: Drive cycle name as store in the data/drive_cycles directory.
        :param folder_dir: The relative path directory to data/drive_cycles.
        """
        if isinstance(drive_cycle_name, str) or (drive_cycle_name is None):
            if isinstance(drive_cycle_name, str):
                self.drive_cycle_name = drive_cycle_name  # insert the name of the .txt file in the relevant directory.
            else:
                self.drive_cycle_name = None
        else:
            TypeError("Drive cycle name needs to a string or None type.")

        if self.drive_cycle_name is not None:
            if isinstance(folder_dir, str):
                if not os.path.exists(folder_dir):
                    raise ValueError(f"{folder_dir} does not exists.")
                else:
                    self.folder_dir = folder_dir
                # if folder_dir[-1] == "/":
                #     self.folder_dir = folder_dir
                # else:
                #     raise ValueError("Drive cycle's folder directory needs to have a '/' at the end.")
            else:
                raise TypeError("Drive cycle's folder directory needs to be a string type.")

            df_drivecycle = self.parse_file()
            self.t = df_drivecycle['Test Time, secs'].to_numpy()  # time array in seconds
            self.speed_mph = df_drivecycle['Target Speed, mph'].to_numpy()  # desired speed, m/h
            self.speed_kmph = df_drivecycle["Target Speed [km/h]"].to_numpy()  # desired speed, km/h
            self.speed_mps = df_drivecycle["Target Speed [m/h]"].to_numpy()  # desired speed, mps
            del df_drivecycle

    def parse_file(self):
        # file_dir = self.folder_dir + f"{self.drive_cycle_name}.txt"
        file_dir = os.path.join(self.folder_dir, f"{self.drive_cycle_name}.csv")
        # df = pd.read_csv(file_dir, sep="\t", skiprows=2, header=None, names=["Test Time [s]", "Target Speed [milesph]"])
        df = pd.read_csv(file_dir)
        df["Target Speed [km/h]"] = df["Target Speed, mph"] * 1.609344  # creates a col with units in km/h
        df["Target Speed [m/h]"] = df["Target Speed [km/h]"] * 1000 / 3600  # creates a col with units in m/s
        return df

    def plot(self):
        """
        Plots the time, s, vs. speed, km/h, plot of the drive cycles.
        :return:
        """
        plt.figure()
        plt.subplot(1, 1, 1)
        plt.plot(self.time_s, self.speed_kmph)
        plt.xlabel('Time [s]')
        plt.ylabel('Speed [km/h]')
        plt.show()

    def __repr__(self):
        return f"DriveCycle({self.drive_cycle_name})"

    def __str__(self):
        return f"{self.drive_cycle_name}"
