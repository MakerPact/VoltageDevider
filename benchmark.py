import mock_sg
import time
from VoltageDevider import find_best_resistor_combinations

start = time.time()
res = find_best_resistor_combinations(Vin=5.0, Vout=3.3, e_series='E96', desired_current=None)
print("E96 no current time:", time.time() - start)

start = time.time()
res = find_best_resistor_combinations(Vin=5.0, Vout=3.3, e_series='E96', desired_current=10.0)
print("E96 with current time:", time.time() - start)
