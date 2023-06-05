import unittest

import numpy as np

import EV_sim


class TestDriveCycleConstructor(unittest.TestCase):
    def test_constructor_with_str_inputs(self):
        t_actual = np.arange(0, 1370)
        udds = EV_sim.DriveCycle(drive_cycle_name="udds")
        self.assertTrue(np.array_equal(t_actual, udds.t))
        self.assertEqual(3.0, udds.speed_mph[21])
        self.assertEqual(4.828032000000000, udds.speed_kmph[21])

    def test_constructor_with_None_inputs(self):
        unknown_drive_cycle = EV_sim.DriveCycle(drive_cycle_name=None)
        self.assertEqual(None, unknown_drive_cycle.drive_cycle_name)

