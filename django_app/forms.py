"""
Contains the classes for the forms to be displayed probably in the index.html
"""
from django import forms

from EV_sim.ev import EVFromDatabase


class SimulationInputForm(forms.Form):
    ev_alias = forms.ChoiceField()
    drive_cycle = forms.ChoiceField()
    air_density = forms.FloatField()
    road_grade = forms.FloatField()
