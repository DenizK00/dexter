#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 20:32:12 2024

@author: deniz
"""

import numpy as np
import pyomo.environ as pyo
import re

from .equation import Equation
from .solution import Solution

class SolverNotInstalled(Exception): pass
class UnrecognizedTerm(Exception): pass


class Problem:

    def __init__(self, objective:str, constraints:list[str], solver="glpk"):
        self.model = self.construct_model(objective, constraints)

        try:
            self.solver = pyo.SolverFactory(solver)
        except:
            raise SolverNotInstalled


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
        self.constraint_matrix = np.vstack([const.to_numpy_array() for const in self.constraints])
        self.definition = f"{self.goal} {self.objective_expr}\n" + "\n".join(str(constraint) for constraint in self.constraints)

        #Do the following conversion from equation to pyomo constraint
        #in the Equation classes method instead of doing here
        set_vars = set()
        for eq in self.constraints:
            for var in eq.variables:
                set_vars.add(var)

        self.variables = sorted(set_vars)

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
        self.solver.solve(self.model)

        optimal_solution = {}
        print("--------- OPTIMAL VALUES ---------")

        for variable in self.variables:
            optimal_val = getattr(getattr(self.model, variable), "value")
            print(f"{variable}:", optimal_val)
            optimal_solution[variable] = optimal_val

        [print("--------------------------------")]

        self.solution = Solution.from_dict(optimal_solution)

        return self.solution
    

    def __call__(self, solution:"Solution or dict"):
        if isinstance(solution, dict):
            solution = Solution(solution)
            # Add try except for other types of variables        

        # Calculate objective value by substituting solution values
        import sympy as sp
        obj_expr = sp.sympify(self.objective_expr)
        
        # Substitute variable values
        for var in self.variables:
            if var in solution:
                obj_expr = obj_expr.subs(var, solution[var])
        
        return float(obj_expr)
    

    def sensitivity(self, b_i:int, solution:"Solution or dict"=None):
        match solution:
            case dict():
                solution = Solution(solution)
            case None:
                solution = getattr(self, "solution", self.solve())
            case Solution():
                pass
            case _:
                raise UnrecognizedTerm("Unrecognized Solution format")
        
        basis = solution.basis

        A_basic = self.constraint_matrix[:, basis]
        A_inv = np.linalg.inv(A_basic)
        beta_i = A_inv[:, b_i]

        # Extract coefficients from objective expression
        import sympy as sp
        obj_expr = sp.sympify(self.objective_expr)
        obj_coeffs = []
        for var in self.variables:
            coeff = obj_expr.coeff(var) if var in obj_expr.free_symbols else 0
            obj_coeffs.append(float(coeff))
        
        c_basic = np.array(obj_coeffs)[basis]
        basic_value = np.sum(c_basic * solution.to_numpy_array()[basis])

        low_bounds, up_bounds = [], []
        decide_append = lambda beta_ij: low_bounds.append(boundary) if beta_ij > 0 else up_bounds.append(boundary)
        for j in range(len(beta_i)):
            print(beta_i[j])
            boundary = round(-solution[j]/beta_i[j], 2)
            print(boundary)
            decide_append(boundary)

        print("Solution remains in the optimal basis while")
        print(f"Delta is within the range: [{max(low_bounds)}, {min(up_bounds)}]")

        # fix the inverted places
        
        return

