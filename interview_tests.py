import unittest
import interview
import numpy as np

class TestInterview(unittest.TestCase):
    def setUp(self):
        self.epsilon = 1e-8

    def test_scalar_is_close(self):
        self.assertTrue(interview.scalar_isclose(0, 0))
        self.assertTrue(interview.scalar_isclose(0, self.epsilon))
        self.assertTrue(interview.scalar_isclose(0, self.epsilon / 10))
        self.assertTrue(interview.scalar_isclose(0.01, 0.01 + self.epsilon))

        self.assertFalse(interview.scalar_isclose(1, 0))
        self.assertFalse(interview.scalar_isclose(-1, 1))
        self.assertFalse(interview.scalar_isclose(0, 0.0009))
        self.assertFalse(interview.scalar_isclose(0, 0.00099999))


    def test_exceeds_overhang(self):
        self.assertTrue(interview.exceeds_overhang(np.array([0, 0, 1])))
        self.assertTrue(interview.exceeds_overhang(np.array([0, 0, -1])))
        self.assertTrue(interview.exceeds_overhang(np.array([0.01, 0.01, -1])))
        self.assertTrue(interview.exceeds_overhang(np.array([0.01, 0.01, 1])))

        self.assertFalse(interview.exceeds_overhang(np.array([0, 0, 0])))
        self.assertFalse(interview.exceeds_overhang(np.array([1, 0, 0])))
        self.assertFalse(interview.exceeds_overhang(np.array([0, 1, 0])))
        self.assertFalse(interview.exceeds_overhang(np.array([1, 1, 0])))

    def test_is_on_build_plate(self):
        self.assertTrue(interview.is_on_build_plate(np.array([0, 0, 0])))
        self.assertTrue(interview.is_on_build_plate(np.array([0, 0, self.epsilon])))
        self.assertTrue(interview.is_on_build_plate(np.array([self.epsilon, self.epsilon, self.epsilon])))
        self.assertTrue(interview.is_on_build_plate(np.array([1, 0, 0])))
        self.assertTrue(interview.is_on_build_plate(np.array([0, 1, 0])))
        self.assertTrue(interview.is_on_build_plate(np.array([2, 1, 0])))

        self.assertFalse(interview.is_on_build_plate(np.array([0, 0, 1])))
        self.assertFalse(interview.is_on_build_plate(np.array([0, 0, self.epsilon * 2])))
        self.assertFalse(interview.is_on_build_plate(np.array([1, 1, 1])))

if __name__ == "__main__":
    unittest.main()
