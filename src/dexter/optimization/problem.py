#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 20:32:12 2024

@author: deniz
"""

import re

import numpy as np
import pyomo.environ as pyo
import sympy as sp

from .equation import Equation
from .solution import Solution

class SolverNotInstalled(Exception): pass
class UnrecognizedTerm(Exception): pass


class Problem:

    def __init__(self, objective:str, constraints:list[str], solver="glpk"):
        self.model = self.construct_model(objective, constraints)

        self.solver_name = solver
        self.solver = pyo.SolverFactory(solver)


    def __str__(self):
        return self.definition
    

    def __repr__(self):
        return f"Problem(objective={self.objective!r}, constraints={self.constraints})"
    

    def construct_model(self, objective, constraints) -> pyo.ConcreteModel:
        model = pyo.ConcreteModel()

        # Parse objective to extract goal (min/max) and equation
        objective_lower = objective.lower().strip()
        
        # Check if objective starts with min/max
        if objective_lower.startswith(('min', 'max')):
            # Extract goal and equation
            goal_match = re.match(r'^(min|max)\s+(.+)', objective_lower)
            if goal_match:
                goal, objective_equation = goal_match.groups()
            else:
                goal, objective_equation = 'min', objective_lower  # Default to minimize
        else:
            # No goal specified, default to minimize
            goal, objective_equation = 'min', objective_lower

        # Create objective function (not a constraint, so don't use Equation class)
        self.objective_expr = objective_equation
        self.goal = goal

        self.constraints = [Equation(c, f"constraint {str(i)}") for i, c in enumerate(constraints)]
        
        # Collect all variables from constraints first
        set_vars = set()
        for eq in self.constraints:
            for var in eq.variables:
                set_vars.add(var)
        
        self.variables = sorted(set_vars)
        
        # Build constraint matrix with consistent variable ordering
        constraint_matrix_rows = []
        for const in self.constraints:
            # Create a row with coefficients for all variables in the problem
            row = []
            for var in self.variables:
                if var in const.variables:
                    row.append(const[var])
                else:
                    row.append(0.0)
            constraint_matrix_rows.append(row)
        
        self.constraint_matrix = np.array(constraint_matrix_rows, dtype=float)
        self.definition = f"{self.goal} {self.objective_expr}\n" + "\n".join(str(constraint) for constraint in self.constraints)

        for var in self.variables:
            setattr(model, var, pyo.Var(domain=pyo.NonNegativeReals))

        obj_expr = re.sub(r"([a-zA-Z]+)", r"model.\1", self.objective_expr)
        model.objective = pyo.Objective(expr=eval(obj_expr), sense=eval(f"pyo.{self.goal}imize"))

        for eq in self.constraints:
            expr = re.sub(r"([a-zA-Z]+)", r"model.\1", str(eq.expr))
            expr = re.sub(r"(?<![\><=])=", "==", expr)
            setattr(model, eq.name.replace(" ", "_"), pyo.Constraint(expr=eval(expr)))

        return model
    
            
    def solve(self) -> "Solution":
        if not self.solver.available(exception_flag=False):
            raise SolverNotInstalled(f"Solver '{self.solver_name}' is not installed.")
        self.solver.solve(self.model)

        optimal_solution = {}
        print("--------- OPTIMAL VALUES ---------")

        for variable in self.variables:
            optimal_val = getattr(getattr(self.model, variable), "value")
            print(f"{variable}:", optimal_val)
            optimal_solution[variable] = optimal_val

        print("--------------------------------")

        self.solution = Solution.from_dict(optimal_solution)

        return self.solution
    

    def __call__(self, solution:"Solution or dict"):
        if isinstance(solution, dict):
            solution = Solution.from_dict(solution)

        # Calculate objective value by substituting solution values
        obj_expr = sp.sympify(self.objective_expr)
        
        # Substitute variable values
        for var in self.variables:
            if var in solution:
                obj_expr = obj_expr.subs(var, solution[var])
        
        return float(obj_expr)
    

    def sensitivity(self, b_i:int, solution:"Solution or dict"=None):
        match solution:
            case dict():
                solution = Solution.from_dict(solution)
            case None:
                solution = self.solution if hasattr(self, "solution") else self.solve()
            case Solution():
                pass
            case _:
                raise UnrecognizedTerm("Unrecognized Solution format")
        
        basis = solution.basis

        A_basic = self.constraint_matrix[:, basis]
        A_inv = np.linalg.inv(A_basic)
        beta_i = A_inv[:, b_i]

        x_basic = solution.to_numpy_array()[basis]

        low_bounds, up_bounds = [], []
        for j in range(len(beta_i)):
            boundary = round(-x_basic[j] / beta_i[j], 2)
            (low_bounds if beta_i[j] > 0 else up_bounds).append(boundary)

        low = max(low_bounds) if low_bounds else -np.inf
        up = min(up_bounds) if up_bounds else np.inf
        print("Solution remains in the optimal basis while")
        print(f"Delta is within the range: [{low}, {up}]")

        return low, up
