import math

# Base E-series values
# I use this as a primer to create the thousands of different values of resistors.
E_SERIES = {
	'E3': [1.0, 2.2, 4.7],
	'E6': [1.0, 1.5, 2.2, 3.3, 4.7, 6.8],
	'E12': [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
	'E24': [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1],
	'E48': [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53],
	'E96': [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]
}
# This function will create all the different resistors baised off of the primes.
def generate_e_series_values(series, min_value, max_value):
		base_values = E_SERIES[series]
		values = []
		for exp in range(math.floor(math.log10(min_value)), math.ceil(math.log10(max_value)) + 1):
				for base in base_values:
						value = base * (10 ** exp)
						if min_value <= value <= max_value:
								values.append(value)
		return sorted(values)
# this is the math behind the selections the user inputs.

def find_best_resistor_combinations(Vin, Vout, e_series, desired_current=None, num_results=20):
		resistors = generate_e_series_values(e_series, 1, 1e6)  # Generate resistors from 1 ohm to 1 Mohm
		target_ratio = Vout / Vin
		combinations = []

		for R1 in resistors:
				for R2 in resistors:
						ratio = R2 / (R1 + R2)
						error = abs(ratio - target_ratio)
						current = Vin / (R1 + R2) * 1000  # Convert to mA
						power = Vin * current / 1000  # Power in mW
						if desired_current:
								current_error = abs(current - desired_current)
								total_error = error + current_error / desired_current
						else:
								total_error = error

						combinations.append((R1, R2, error, current, power, total_error))

		combinations.sort(key=lambda x: x[5])  # Sort by total error


		# Remove redundant combinations like powers of 10, 100, 1000 ....
		unique_combinations = []
		seen_ratios = set()
		for combo in combinations:
				R1, R2 = combo[0], combo[1]
				ratio = R2 / (R1 + R2)
				rounded_ratio = round(ratio, 4)  # Round to 4 decimal places for comparison. Can be closer but seams redundant.
				if rounded_ratio not in seen_ratios:
						seen_ratios.add(rounded_ratio)
						unique_combinations.append(combo)
				if len(unique_combinations) == num_results:
						break

		return unique_combinations

# Modify the existing calculate_voltage_divider function:
def calculate_voltage_divider(Vin, Vout, R1, R2, e_series, desired_current=None):
		if Vin and Vout and not R1 and not R2:
				combinations = find_best_resistor_combinations(Vin, Vout, e_series, desired_current)
				return combinations
		elif Vin and R1 and R2 and not Vout:
				Vout = Vin * (R2 / (R1 + R2))
		elif Vin and Vout and R2 and not R1:
				R1 = R2 * ((Vin / Vout) - 1)
		elif Vin and Vout and R1 and not R2:
				R2 = R1 / ((Vin / Vout) - 1)
		elif Vout and R1 and R2 and not Vin:
				Vin = Vout * ((R1 + R2) / R2)
		else:
				return None
		return [(R1, R2, 0)]  # Return as a list fo
def main():
		# Create the layout for all of the objects that will be used in the app.
		layout = [
				[sg.Text('Voltage Divider Calculator', font=('Arial', 20))],
				[sg.Text('Input Voltage (Vin):', size=(15, 1)), sg.InputText(key='-VIN-')],
				[sg.Text('Output Voltage (Vout):', size=(15, 1)), sg.InputText(key='-VOUT-')],
				[sg.Text('Desired Current (mA):', size=(15, 1)), sg.InputText(key='-CURRENT-')],
				[sg.Text('R1 (Ω):', size=(15, 1)), sg.InputText(key='-R1-')],
				[sg.Text('R2 (Ω):', size=(15, 1)), sg.InputText(key='-R2-')],
				[sg.Text('E-Series:', size=(15, 1)), sg.Combo(['E3', 'E6', 'E12', 'E24', 'E48', 'E96'], default_value='E24', key='-ESERIES-')],
				[sg.Button('Calculate'), sg.Button('Clear')],
				[sg.Text('Results:', font=('Arial', 16))],
				[sg.Table(values=[], headings=['Rank', 'R1 (Ω)', 'R2 (Ω)', 'Vout (V)', 'Current (mA)', 'Power (mW)', 'Error (%)'],
									auto_size_columns=False,
									col_widths=[5, 10, 10, 10, 12, 12, 10],
									justification='right',
									num_rows=20,
									key='-RESULTS-',
									alternating_row_color='#2C2F33',
									text_color='#FFFFFF',
									background_color='#36393F',
									enable_events=True)]
		]

		# make the window, and populate it with all of the objects.
		window = sg.Window('VoltageDevider', layout, finalize=True, resizable=True, size=(800, 600))
		while True:
				event, values = window.read()
				if event == sg.WINDOW_CLOSED:
						break
				elif event == 'Calculate':
						Vin = float(values['-VIN-']) if values['-VIN-'] else None
						Vout = float(values['-VOUT-']) if values['-VOUT-'] else None
						R1 = float(values['-R1-']) if values['-R1-'] else None
						R2 = float(values['-R2-']) if values['-R2-'] else None
						e_series = values['-ESERIES-']
						desired_current = float(values['-CURRENT-']) if values['-CURRENT-'] else None

						result = calculate_voltage_divider(Vin, Vout, R1, R2, e_series, desired_current)
						if result:
								table_data = []
								for i, values in enumerate(result, 1):
										R1, R2, error, *rest = values + (None, None, None)
										current = rest[0] if rest else None
										power = rest[1] if len(rest) > 1 else None

										Vout_calc = Vin * (R2 / (R1 + R2)) if Vin else 0
										table_data.append([


			i,
			f"{R1:.2f}" if R1 is not None else "N/A",
			f"{R2:.2f}" if R2 is not None else "N/A",
			f"{Vout_calc:.2f}" if Vout_calc is not None else "N/A",
			f"{current:.2f}" if current is not None else "N/A",
			f"{power:.2f}" if power is not None else "N/A",

		])

								window['-RESULTS-'].update(values=table_data)
						else:
								sg.popup('Insufficient data. Please provide Vin and Vout, or three out of Vin, Vout, R1, and R2.')
				elif event == 'Clear':
						for key in ('-VIN-', '-VOUT-', '-CURRENT-', '-R1-', '-R2-'):
								window[key].update('')
						window['-RESULTS-'].update(values=[])

	window.close()

if __name__ == '__main__':
		main()
