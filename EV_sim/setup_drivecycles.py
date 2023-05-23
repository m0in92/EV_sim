import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Drive_cycle:
    def __init__(self, drive_cycle_name = "udds"):
        self.drive_cycle_name = drive_cycle_name # insert the name of the .txt file in the relevant directory.

    def parse_file(self):
        file_dir = file_dir = f"data/drive_cycles/{self.drive_cycle_name}.txt"
        df = pd.read_csv(file_dir, sep="\t", skiprows=2, header=None, names=["Test Time [s]", "Target Speed [milesph]"])
        df["Target Speed [km/h]"] = df["Target Speed [milesph]"] * 1.609344 # creates a col with units in km/h
        df["Target Speed [m/h]"] = df["Target Speed [km/h]"] * 1000/3600  # creates a col with units in m/s
        return df

    @property
    def time_s(self):
        return np.array(self.parse_file()["Test Time [s]"])

    @property
    def speed_kmph(self):
        return np.array(self.parse_file()["Target Speed [km/h]"])

    @property
    def speed_mps(self):
        return np.array(self.parse_file()["Target Speed [m/h]"])


    def plot(self):
        plt.figure()
        plt.subplot(1,1,1)
        plt.plot(self.time_s, self.speed_kmph)
        plt.xlabel('Time [s]')
        plt.ylabel('Speed [km/h]')
        plt.show()

    def __repr__(self):
        return f"{self.drive_cycle_name}"

    def __str__(self):
        return f"{self.drive_cycle_name}"