#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 19:44:27 2024

@author: deniz
"""

from pyomo.environ import *

# Define model
model = ConcreteModel()

# Cost parameters
c = 5  # cost per unit ordered
b = 7  # cost per unit when demand exceeds the order
h = 3  # holding cost per unit when order exceeds demand

# Demand scenarios and their probabilities
demands = [80, 95, 120]
probabilities = [0.5, 0.4, 0.1]

# Decision variable for order quantity
model.x = Var(domain=NonNegativeReals)

# Objective function to minimize expected cost
def objective_rule(model):
    return sum(probabilities[i] * (c * model.x +
                                   h * max(0, model.x - demands[i]) +
                                   b * max(0, demands[i] - model.x))
               for i in range(len(demands)))

model.cost = Objective(rule=objective_rule, sense=minimize)

# Solver options
solver = SolverFactory('ipopt')  # You can also use 'glpk', 'cplex', etc.
solver.solve(model)

# Output the optimal order quantity and the minimum expected cost
optimal_x = model.x.value
min_cost = model.cost()

print(f"Optimal Order Quantity: {optimal_x:.2f}")
print(f"Minimum Expected Cost: {min_cost:.2f}")
