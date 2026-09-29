import PySimpleGUI as sg
from unittest.mock import patch
import sys

# Patch sg.Window so we can intercept calls without opening GUI
class MockWindow:
    def __init__(self, *args, **kwargs):
        self.count = 0
    def read(self):
        self.count += 1
        if self.count == 1:
            # First event: calculate with invalid float
            return 'Calculate', {'-VIN-': 'abc', '-VOUT-': '5', '-R1-': '', '-R2-': '', '-ESERIES-': 'E24', '-CURRENT-': ''}
        else:
            # Second event: window closed
            return sg.WINDOW_CLOSED, {}
    def close(self):
        pass

@patch('PySimpleGUI.Window', return_value=MockWindow())
@patch('PySimpleGUI.popup_error')
def test_validation(mock_popup, mock_window):
    try:
        import VoltageDevider
    except Exception as e:
        print(f"Exception raised: {e}")
        sys.exit(1)

    mock_popup.assert_called_once_with('Invalid input: Please enter valid numerical values.', title='Error')
    print("Test passed: popup_error was called and no exception was raised!")

if __name__ == "__main__":
    test_validation()
