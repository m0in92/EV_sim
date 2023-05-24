import unittest

import numpy as np

import EV_sim


class TestDriveCycle(unittest.TestCase):
    def test_constructor(self):
        t_actual = np.arange(0, 1370)
        udds = EV_sim.DriveCycle()
        self.assertTrue(np.array_equal(t_actual, udds.t))
        self.assertEqual(3.0, udds.speed_mph[21])
        self.assertEqual(4.828032000000000, udds.speed_kmph[21])