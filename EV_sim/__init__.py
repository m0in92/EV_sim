"""
Package header for EV_sim namespace
Provides the simulations for the Electric Vehicle dynamic simulations
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by EV_sim. All rights reserved."


from .ev import EV, EVFromDatabase
from .extern_conditions import ExternalConditions
from .drivecycles import DriveCycle
from .model import VehicleDynamics
# from gui_dir.gui import VehicleDynamicsApp
from .tkinter_gui.main import VehicleDynamicsApp
