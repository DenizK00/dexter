#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 19:46:22 2024

@author: deniz
"""

import re
import numpy as np
import pandas as pd
import copy

class Equation:
    def __init__(self, expr: str, name=None):
        self.name = name
        self.expr = expr
        self.validate_expression()
        self.terms = self.parse_terms()
        self.var_to_coef = self.extract_terms()

    def __str__(self) -> str:
        return self.expr

    def validate_expression(self):
        seperator_pattern = r"(>=|<=|=)"
        exprs = re.split(seperator_pattern, self.expr)

        if len(exprs) != 3:
            raise ValueError("Invalid expression format. Ensure the expression includes an operator and both sides.")

        self.LHS, self.SEP, self.RHS = exprs

        if self.SEP not in ["<=", ">=", "="]:
            raise ValueError("Unsupported operator. Only <=, >=, and = are supported.")

    def parse_terms(self) -> list[tuple]:
        # Regex to capture terms with optional leading signs, coefficients, and variable names
        pattern = r"([+-]?)\s*(\d+)?([a-zA-Z]+)\^?(\d+)?"
        return re.findall(pattern, self.LHS)

    def extract_terms(self) -> dict[str, float]:
        var_to_coef = {t[2]: float(t[1])*(-1 if t[0] == '-' else 1) for t in self.terms if t[1]}
        # self.add_slack_variable()
        if self.RHS:
            var_to_coef["constant"] = -float(self.RHS)

        self.variables = list(var_to_coef.keys())
        self.coefficients = np.array(list(var_to_coef.values()))
        
        return var_to_coef

    def add_slack_variable(self):
        new_eq = copy.deepcopy(self)
        new_eq.variables.append("slack")
        new_eq.coefficients = np.append(new_eq.coefficients, [1])
        # Change slack variable assignment
        # Change Equation format maybe, Ways to represent the LHS and RHS and the relation in one form
        
        if self.SEP == ">=":
            new_expr = self.expr.replace(">=", "=") + " - slack"
        
        elif self.SEP == "<=":
            new_expr = self.expr.replace("<=", "=") + " + slack"
        
        return Equation(new_expr, self.name)
    

    def to_numpy_array(self) -> np.array:
        return np.array(self.coefficients)

    def to_pandas_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self.coefficients], columns=self.variables, index=[self.name + ":"])

# Example usage
equation = "3x + 5y - 2z >= 10"
eq = Equation(equation, name="constraint 1")
print(eq)
print(eq.add_slack_variable())