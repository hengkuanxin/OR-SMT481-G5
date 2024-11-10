# if you don't have pulp installed, run the following command:
# pip install pulp

import pulp
from random import randint
from helpers import get_manhattan_stations, add_benefit_score

# Load Manhattan stations data
data = get_manhattan_stations()    
stations_dict = add_benefit_score(data)
# print(len(stations_dict))
# print(stations_dict)

# Step 1: Define the model
model = pulp.LpProblem("Bike_Redistribution_Optimization", pulp.LpMaximize)

# Step 2: Define constants and parameters
num_stations = 662  # Total number of stations (0 to 612)
c_unit = 3  # Unit cost to relocate a bike
M = 100000  # Large constant for big-M constraint
e = 0.00001 # Small constant for strictly positive constraint (for w)
F = 37369 # Total number of bikes in the fleet (as of Sep 2024)

b = [stations_dict[k]['benefit_value'] for k in stations_dict]  # Benefit per bike at each station
C = [stations_dict[k]['capacity'] for k in stations_dict]  # Capacity of each station
n = [randint(0, cap) for cap in C]  # Current number of bikes at each station (example)

print("Benefit", b[:10])
print("Capacity", C[:10])
print("Current number of bikes", n[:10])

# Step 3: Define decision variables
x = pulp.LpVariable.dicts("x", range(num_stations), lowBound=0, cat='Integer')
abs = pulp.LpVariable.dicts("abs", range(num_stations), lowBound=0, cat='Integer')
w = pulp.LpVariable("w", cat='Binary')

# Step 4: Define the objective function
model += pulp.lpSum([b[i] * x[i] for i in range(num_stations)]) - pulp.lpSum([c_unit * abs[i] for i in range(num_stations)])

# Step 5: Define the constraints
# Capacity constraint: x_i <= C_i for all stations
for i in range(num_stations):
    model += x[i] <= C[i]

# Absolute value constraint: abs_i >= |x_i - n_i|
for i in range(num_stations):
    model += abs[i] >= x[i] - n[i]
    model += abs[i] >= n[i] - x[i]

# Fleet size constraint:
model += pulp.lpSum([x[i] for i in range(num_stations)]) <= F

# Big-M constraints to determine the value of w:
model += pulp.lpSum([b[i] * x[i] for i in range(num_stations)]) - \
         pulp.lpSum([c_unit * abs[i] for i in range(num_stations)]) >= e - M * (1 - w)

model += pulp.lpSum([b[i] * x[i] for i in range(num_stations)]) - \
         pulp.lpSum([c_unit * abs[i] for i in range(num_stations)]) <= -e + (M * w)

# Step 6: Solve the model
solver = pulp.PULP_CBC_CMD(timeLimit=300, gapRel=0.01) # Times out the solver within 300ms and accepts solutions within 1% of the optimal solution
model.solve(solver)

# Step 7: Output the results
print("Status:", pulp.LpStatus[model.status])
print("Calculated Net Benefit:", pulp.value(model.objective))
print(f"Should redistribute? {'Yes' if w.value() == 1 else 'No'}")

# Print optimal bike allocations if redistribution happens
if w.value() == 1:
    print("Optimal bike allocations:")
    for i in range(num_stations):
        print(f"Station {i}: Allocate {x[i].value()} bikes")
