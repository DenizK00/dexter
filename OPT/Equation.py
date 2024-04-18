#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 19:46:22 2024

@author: deniz
"""

import re
import numpy as np

class Equation:
    def __init__(self, expr: str):
        self.expr = expr
        self.terms = self.parse_terms()
        self.variables, self.coefficients = self.extract_terms()

    def parse_terms(self):
        exprs = self.expr.split("=")
        self.LHS = exprs[0]
        self.RHS = exprs[1] if len(exprs) == 2 else None

        # Regex to capture terms with optional leading signs, coefficients, and variable names
        pattern = r'([+-]?)\s*(\d+)([a-zA-Z]+)'
        return re.findall(pattern, self.LHS)


    def extract_terms(self):
        var_to_coef = {t[2]:float(t[1])*(-1 if t[0] == "-" else 1) for t in self.terms}

        variables = np.array(list(var_to_coef.keys()))
        coefficients = np.array(list(var_to_coef.values()))

        return variables, coefficients


    def to_Vector(self):
        # Create a list of coefficients based on sorted variables
        row = [self.coefficients.get(var, 0) for var in sorted(self.variables)]
        row.append(self.coefficients.get('constant', 0))  # Append the constant term
        return np.array(row) 
    
    def to_Series(self):
        pass


# Example usage
equation = "3x_1 + 5y - 2z - 4a"
eq = Equation(equation)
print(eq.variables)