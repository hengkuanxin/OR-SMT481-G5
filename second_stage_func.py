import pandas as pd
import numpy as np
import pulp
import random
from first_stage_func import first_stage

def second_stage(current_station):
    first_stage_results = first_stage(current_station)
    allocation = first_stage_results[2]
    
    data_directory = 'datasets/'
    stations = current_station
    percentage_map = {
        'Lowest': 0.20,
        'Low': 0.40,
        'Medium': 0.60,
        'Highest': 0.80
    }
    stations['DEMAND'] = stations['DEMAND_CATEGORY'].map(percentage_map) * stations['capacity']
    distance_matrix = pd.read_csv(f'{data_directory}/distance_matrix.csv', index_col=0).to_numpy()
        
    # Parameters
    S = len(stations)  # Number of bike stations (adjust as needed)
    scenarios = ["Cloudy", "Rainy", "Sunny", "Clear"]
    probabilities = {
        "Cloudy": 0.3, 
        "Rainy": 0.2, 
        "Sunny": 0.1, 
        "Clear": 0.4
    }
    penalty_unmet_demand = 1000  # Penalty for unmet demand
    penalty_over_capacity = 500  # Penalty for exceeding capacity

    # Randomly generated input data
    cij = distance_matrix # Cost matrix for relocation
    A = sum(allocation)  # Total initial bike allocation
    initial_bikes = allocation
    Ci = stations["capacity"]  # Capacity for each station
    Di = stations["DEMAND"]
    weather_factors = {
        "Cloudy": 0.8, 
        "Rainy": 1.2, 
        "Sunny": 1.0, 
        "Clear": 0.9
    }

    # Decision Variables
    model = pulp.LpProblem("Bike_Relocation_Optimization", pulp.LpMinimize)
    yijk = pulp.LpVariable.dicts("yijk", [(i, j, k) for i in range(S) for j in range(S) for k in scenarios], lowBound=0, cat='Integer')
    xik = pulp.LpVariable.dicts("xik", [(i, k) for i in range(S) for k in scenarios], lowBound=0, cat='Integer')

    # Penalty Variables
    unmet_demand = pulp.LpVariable.dicts("unmet_demand", [(i, k) for i in range(S) for k in scenarios], lowBound=0, cat='Integer')
    over_capacity = pulp.LpVariable.dicts("over_capacity", [(i, k) for i in range(S) for k in scenarios], lowBound=0, cat='Integer')

    # Objective Function: Minimize relocation cost + penalties
    model += (
        pulp.lpSum(yijk[i, j, k] * cij[i][j] * probabilities[k] for i in range(S) for j in range(S) for k in scenarios) +
        penalty_unmet_demand * pulp.lpSum(unmet_demand[i, k] for i in range(S) for k in scenarios) +
        penalty_over_capacity * pulp.lpSum(over_capacity[i, k] for i in range(S) for k in scenarios)
    )
    # print("Model as been defined.")

    # Constraints

    # Total allocation for each scenario cannot exceed initial allocation
    for k in scenarios:
        model += pulp.lpSum(xik[i, k] for i in range(S)) <= A, f"Allocation_Constraint_Scenario_{k}"
    # print("Constraint 1 Defined.")

    # Define final number of bikes with relaxed constraint
    for i in range(S):
        for k in scenarios:
            model += xik[i, k] == initial_bikes[i] + pulp.lpSum(yijk[j, i, k] for j in range(S)) - pulp.lpSum(yijk[i, j, k] for j in range(S)), f"Final_Bikes_Constraint_{i}_{k}"
    # print("Constraint 2 Defined.")

    # Demand satisfaction with penalties
    for i in range(S):
        for k in scenarios:
            expected_demand = Di[i] * weather_factors[k]
            model += xik[i, k] + unmet_demand[i, k] >= expected_demand, f"Demand_Constraint_{i}_{k}"
    # print("Constraint 3 Defined.")

    # Capacity constraint with penalties
    for i in range(S):
        for k in scenarios:
            model += xik[i, k] - over_capacity[i, k] <= Ci[i], f"Capacity_Constraint_{i}_{k}"
    # print("Constraint 4 Defined.")

    # Solve the model
    # print("Solving...")
    status = model.solve()

    # Output results
    # if status == pulp.LpStatusOptimal:
    #     print(f"Optimal Solution Found with Total Cost: {pulp.value(model.objective):.2f}")
    # else:
    #     print("No optimal solution found.")
        
    
    # Output results
    if status == pulp.LpStatusOptimal:
        # print(f"Optimal Solution Found with Total Cost: {pulp.value(model.objective):.2f}\n")
        
        # # Print the allocation, unmet demand, and over-capacity penalties for each station and scenario
        # print("Bike Allocations, Unmet Demand, and Over Capacity Penalties:")
        # for i in range(S):
        #     for k in scenarios:
        #         print(f"Station {i}, Scenario {k}:")
        #         print(f"  Bikes Allocated (xik) = {xik[i, k].varValue}")
        #         print(f"  Unmet Demand Penalty = {unmet_demand[i, k].varValue}")
        #         print(f"  Over Capacity Penalty = {over_capacity[i, k].varValue}")
        # print("\nRelocation Plan:")

        # Print the relocation details (yijk) only if bikes are being relocated
        relocation_list = []
        current_weather = ''
        random_factor = random.randint(0,10000)
        if random_factor < 3000:
            current_weather = 'Cloudy'
        elif random_factor < 5000:
            current_weather = 'Rainy'
        elif random_factor < 6000:
            current_weather = 'Sunny'
        else: current_weather = 'Clear'
        for k in scenarios:
            # print(f"\nScenario {k} Relocations:")
            if current_weather != k:
                continue
            relocation_count = 0
            for i in range(S):
                for j in range(S):
                    if i != j and yijk[i, j, k].varValue > 0:
                        relocation_list.append((yijk[i, j, k].varValue,i,j))
                        # print(f"  Relocate {yijk[i, j, k].varValue} bikes from Station {i} to Station {j}")
                        relocation_count += 1
            # if relocation_count == 0:
            #     print("  No relocations needed for this scenario.")
    # else:
    #     print("No optimal solution found.")
        
    return [pulp.value(model.objective), relocation_list]

    
    