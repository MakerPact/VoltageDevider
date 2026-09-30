import unittest
from VoltageDevider import calculate_voltage_divider

class TestVoltageDividerEdgeCases(unittest.TestCase):
    def test_equal_voltage_inputs(self):
        """Test with Vin == Vout, should raise ZeroDivisionError when solving for R2."""
        with self.assertRaises(ZeroDivisionError):
            calculate_voltage_divider(Vin=5.0, Vout=5.0, R1=1000, R2=None, e_series='E24')

    def test_zero_voltage_inputs(self):
        """Test with zero voltage inputs, which currently evaluate to False and return None."""
        # Vin = 0
        self.assertIsNone(calculate_voltage_divider(Vin=0.0, Vout=5.0, R1=1000, R2=None, e_series='E24'))
        # Vout = 0
        self.assertIsNone(calculate_voltage_divider(Vin=5.0, Vout=0.0, R1=None, R2=1000, e_series='E24'))

if __name__ == '__main__':
    unittest.main()
