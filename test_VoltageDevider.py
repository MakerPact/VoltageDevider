import unittest
import math
from VoltageDevider import generate_e_series_values

class TestVoltageDevider(unittest.TestCase):

    def test_e3_series(self):
        # Generate E3 series values from 1 to 10
        # Expected: 1.0, 2.2, 4.7, 10.0
        values = generate_e_series_values('E3', 1, 10)
        self.assertEqual(values, [1.0, 2.2, 4.7, 10.0])

    def test_e6_series(self):
        # Generate E6 series values from 1 to 100
        values = generate_e_series_values('E6', 1, 100)
        expected = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8, 10.0, 15.0, 22.0, 33.0, 47.0, 68.0, 100.0]
        self.assertEqual(values, expected)

    def test_min_max_bounds(self):
        # Test boundaries correctly applied
        # From 2.0 to 5.0 for E3
        values = generate_e_series_values('E3', 2.0, 5.0)
        self.assertEqual(values, [2.2, 4.7])

    def test_exponents(self):
        # Test large and small values
        # e.g. from 100 to 1000 for E3
        values = generate_e_series_values('E3', 100, 1000)
        expected = [100.0, 220.0, 470.0, 1000.0]
        self.assertEqual(len(values), len(expected))
        for v, e in zip(values, expected):
            self.assertAlmostEqual(v, e)

        # Test small values 0.1 to 1
        values = generate_e_series_values('E3', 0.1, 1.0)
        # Note: floating point multiplication might result in e.g. 0.22000000000000003
        # So let's check with almost equal
        expected = [0.1, 0.22, 0.47, 1.0]
        self.assertEqual(len(values), len(expected))
        for v, e in zip(values, expected):
            self.assertAlmostEqual(v, e)

    def test_empty_generation(self):
        # If bounds don't cover any base value in the given exponents
        # Wait, if bounds are e.g., 1.1 to 2.1 for E3 (bases: 1.0, 2.2, 4.7)
        values = generate_e_series_values('E3', 1.1, 2.1)
        self.assertEqual(values, [])

if __name__ == '__main__':
    unittest.main()
