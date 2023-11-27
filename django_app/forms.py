"""
Contains the classes for the forms to be displayed probably in the index.html
"""
import os
import glob

from django import forms

from EV_sim.config import definations
from EV_sim.ev import EVFromDatabase


class SimulationInputForm(forms.Form):
    DRIVE_CYCLE_WILDCARD = glob.glob(os.path.join('EV_sim', 'data', 'drive_cycles', '*.csv'))

    lst_choices_ev_alias: tuple = [(ev_alias, ev_alias) for ev_alias in
                                 EVFromDatabase.list_all_EV_alias(file_dir=definations.EV_DATA_DIR)]
    lst_choices_drive_cycles: tuple = [(drive_cycle.split("\\")[-1].split('.')[0],
                                        drive_cycle.split("\\")[-1].split('.')[0])
                                       for drive_cycle in DRIVE_CYCLE_WILDCARD]

    ev_alias = forms.ChoiceField(choices=lst_choices_ev_alias)
    drive_cycle = forms.ChoiceField(choices=lst_choices_drive_cycles)
    air_density = forms.FloatField()
    road_grade = forms.FloatField()
