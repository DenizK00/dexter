#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 20:32:12 2024

@author: deniz
"""

import pyomo.environ as pyo


class SolverNotInstalled(Exception): pass


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

        obj_split = re.split(r"(?<=^m[a-zA-Z]{2})", objective.lower(), maxsplit=1)
        goal, objective_equation = obj_split[0], obj_split[1] ###CHANGE GOAL

        self.objective = Equation(objective_equation, name=f"objective {goal}")

        self.constraints = [Equation(c, f"constraint {str(i)}") for i, c in enumerate(constraints)]

        self.definition = str(self.objective) + "\n" + "\n".join(str(constraint) for constraint in self.constraints)

        #Do the following conversion from equation to pyomo constraint
        #in the Equation classes method instead of doing here
        set_vars = set()
        for eq in self.constraints:
            for var in eq.variables:
                set_vars.add(var)

        self.variables = sorted(set_vars)

        for var in self.variables:
            setattr(model, var, pyo.Var(domain=pyo.NonNegativeReals))

        obj_expr = re.sub(r"([a-zA-Z])", r"*model.\1", self.objective.expr)
        model.objective = pyo.Objective(expr=eval(obj_expr), sense=eval(f"pyo.{goal}imize"))

        for eq in self.constraints:
            expr = re.sub(r"([a-zA-Z])", r"*model.\1", eq.expr)
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

        value = np.sum(self.objective.to_numpy_array() * solution.to_numpy_array())
        return value
