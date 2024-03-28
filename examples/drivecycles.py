#  Copyright (c) 2024. Moin Ahmed. All Rights Reserved.

"""
Contains the scripts for plotting various available EV drive-cycles.
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df_us06: pd.DataFrame = pd.read_csv(os.path.join("..", "EV_sim", "data", "drive_cycles", "us06.csv"))
t_us06: np.ndarray = df_us06['Test Time, secs'].to_numpy()
v_us06: np.ndarray = df_us06['Target Speed, mph'].to_numpy()

df_hwfet: pd.DataFrame = pd.read_csv(os.path.join("..", "EV_sim", "data", "drive_cycles", "hwfet.csv"))
t_hwfet: np.ndarray = df_hwfet['Test Time, secs'].to_numpy()
v_hwfet: np.ndarray = df_hwfet['Target Speed, mph'].to_numpy()

df_udds: pd.DataFrame = pd.read_csv(os.path.join("..", "EV_sim", "data", "drive_cycles", "udds.csv"))
t_udds: np.ndarray = df_udds['Test Time, secs'].to_numpy()
v_udds: np.ndarray = df_udds['Target Speed, mph'].to_numpy()

df_nycc: pd.DataFrame = pd.read_csv(os.path.join("..", "EV_sim", "data", "drive_cycles", "nycc.csv"))
t_nycc: np.ndarray = df_nycc['Test Time, secs'].to_numpy()
v_nycc: np.ndarray = df_nycc['Target Speed, mph'].to_numpy()

df_ftp: pd.DataFrame = pd.read_csv(os.path.join("..", "EV_sim", "data", "drive_cycles", "ftp.csv"))
t_ftp: np.ndarray = df_ftp['Test Time, secs'].to_numpy()
v_ftp: np.ndarray = df_ftp['Target Speed, mph'].to_numpy()

df_bcdc: pd.DataFrame = pd.read_csv(os.path.join("..", "EV_sim", "data", "drive_cycles", "bcdc.csv"))
t_bcdc: np.ndarray = df_bcdc['Test Time, secs'].to_numpy()
v_bcdc: np.ndarray = df_bcdc['Target Speed, mph'].to_numpy()

fig = plt.figure(figsize=(10/1.5, 12.5/1.5))
ax1 = fig.add_subplot(321)
ax1.plot(t_us06, v_us06)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Speed [mph]')
ax1.set_title('US06')

ax2 = fig.add_subplot(322)
ax2.plot(t_hwfet, v_hwfet)
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Speed [mph]')
ax2.set_title('HWFET')

ax3 = fig.add_subplot(323)
ax3.plot(t_udds, v_udds)
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Speed [mph]')
ax3.set_title('UDDS')

ax4 = fig.add_subplot(324)
ax4.plot(t_nycc, v_nycc)
ax4.set_xlabel('Time [s]')
ax4.set_ylabel('Speed [mph]')
ax4.set_title('NYCC')

ax5 = fig.add_subplot(325)
ax5.plot(t_ftp, v_ftp)
ax5.set_xlabel('Time [s]')
ax5.set_ylabel('Speed [mph]')
ax5.set_title('FTP')

ax6 = fig.add_subplot(326)
ax6.plot(t_bcdc, v_bcdc)
ax6.set_xlabel('Time [s]')
ax6.set_ylabel('Speed [mph]')
ax6.set_title('BCDC')

plt.tight_layout()
plt.show()
