import unittest
import sys
import os

# Add the parent directory to the path so we can import VoltageDevider
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from VoltageDevider import calculate_voltage_divider, find_best_resistor_combinations

class TestVoltageDivider(unittest.TestCase):
    """
    Test cases for VoltageDevider edge cases, focusing on zero or equal voltage inputs.
    """

    def test_zero_voltage_inputs(self):
        """
        Test that calculate_voltage_divider gracefully handles zero voltage inputs
        by falling through to the `else` block (since `if Vin and Vout` is falsy).
        """
        # Vin = 0
        res = calculate_voltage_divider(Vin=0, Vout=5, R1=None, R2=None, e_series='E24')
        self.assertIsNone(res)

        # Vout = 0
        res = calculate_voltage_divider(Vin=5, Vout=0, R1=None, R2=None, e_series='E24')
        self.assertIsNone(res)

        # Vin = 0 and Vout = 0
        res = calculate_voltage_divider(Vin=0, Vout=0, R1=100, R2=None, e_series='E24')
        self.assertIsNone(res)

    def test_vin_equals_vout_division_by_zero(self):
        """
        When Vin == Vout and R1 is provided, calculating R2 involves division by
        ((Vin / Vout) - 1), which evaluates to 0 and causes a ZeroDivisionError.
        """
        with self.assertRaises(ZeroDivisionError):
            calculate_voltage_divider(Vin=10.0, Vout=10.0, R1=100.0, R2=None, e_series='E24')

    def test_vin_equals_vout_r2_provided(self):
        """
        When Vin == Vout and R2 is provided, calculating R1 evaluates to
        R2 * ((Vin / Vout) - 1) = 0.0, which is physically correct (a wire).
        """
        res = calculate_voltage_divider(Vin=10.0, Vout=10.0, R1=None, R2=100.0, e_series='E24')
        self.assertEqual(res, [(0.0, 100.0, 0)])

    def test_find_best_resistor_combinations_zero_vin(self):
        """
        When Vin == 0 in find_best_resistor_combinations, calculating the
        target_ratio involves division by Vin, causing a ZeroDivisionError.
        """
        with self.assertRaises(ZeroDivisionError):
            find_best_resistor_combinations(Vin=0, Vout=5, e_series='E24')

if __name__ == '__main__':
    unittest.main()
