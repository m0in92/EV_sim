import unittest

import numpy as np

import EV_sim


class TestExternalConditions(unittest.TestCase):
    def test_constructor(self):
        waterloo = EV_sim.ExternalConditions(rho=1.225, road_grade=0.3)
        self.assertEqual(1.225, waterloo.rho)
        self.assertEqual(0.3, waterloo.road_grade)
        self.assertEqual(np.arctan(0.3/100), waterloo.road_grade_angle)
        self.assertEqual(0.0, waterloo.road_force)