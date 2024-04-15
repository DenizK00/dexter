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
        # Regex to capture terms with optional leading signs, coefficients, and variable names
        pattern = r'([-+]?[\d]*)([a-zA-Z_]\w*)|([-+]?\b\d+\b)'
        print(re.findall(pattern, self.expr))
        return re.findall(pattern, self.expr)

    def extract_terms(self):
        variables = []
        coefficients = {}
        
        for term in self.terms:
            if term[1]:  # Term with a variable
                coefficient = term[0] if term[0] not in ['', '+', '-'] else ('-1' if term[0] == '-' else '1')
                if term[1] not in variables:
                    variables.append(term[1])
                coefficients[term[1]] = int(coefficient)
            elif term[2]:  # Constant term
                coefficients['constant'] = int(term[2])

        return variables, coefficients

    def to_row_vector(self):
        # Create a list of coefficients based on sorted variables
        row = [self.coefficients.get(var, 0) for var in sorted(self.variables)]
        row.append(self.coefficients.get('constant', 0))  # Append the constant term
        return np.array(row)  # Return as a NumPy array

# Example usage
equation = "3x_1 + 5y + 2z + 1 - 4a"
eq = Equation(equation)
row_vector = eq.to_row_vector()
print(equation)
print("Variables:", eq.variables)
print("Row vector form:", row_vector)
