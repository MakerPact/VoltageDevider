import sys
import mock_sg

class MockWindow:
    def __init__(self, *args, **kwargs):
        pass
    def read(self):
        return 'Calculate', {
            '-VIN-': '5.0',
            '-VOUT-': '3.3',
            '-R1-': '',
            '-R2-': '',
            '-ESERIES-': 'E24',
            '-CURRENT-': ''
        }
    def __getitem__(self, key):
        return mock_sg.mock.MagicMock()
    def close(self):
        pass

mock_window_instance = MockWindow()

def mock_window_func(*args, **kwargs):
    return mock_window_instance

mock_sg.mock.MagicMock().Window = mock_window_func
sys.modules['PySimpleGUI'] = mock_sg.mock.MagicMock()

import PySimpleGUI
PySimpleGUI.Window = mock_window_func

def mock_read():
    return PySimpleGUI.WINDOW_CLOSED, {}

mock_window_instance.read = mock_read

from VoltageDevider import find_best_resistor_combinations

# test find_best_resistor_combinations no desired_current
res = find_best_resistor_combinations(Vin=5.0, Vout=3.3, e_series='E24')
assert len(res) == 20
for r in res:
    assert len(r) == 6

print("All tests passed!")
