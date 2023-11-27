"""
Contains the url patterns for the django app.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by Moin Ahmed. All rights reserved."

from django.urls import path
from . import views


urlpatterns: list = [
    path('', views.index, name='index')
]

