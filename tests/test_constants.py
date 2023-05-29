import unittest

from EV_sim.constants import PhysicsConstants


class TestPhysicsConstants(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual(9.81, PhysicsConstants.g)
