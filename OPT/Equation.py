#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 19:46:22 2024

@author: deniz
"""

import re
import numpy as np
import pandas as pd

class Equation:
    def __init__(self, expr: str, name=None):
        self.expr = expr
        self.terms = self.parse_terms()
        self.var_to_coef = self.extract_terms()


    def __repr__(self) -> str:
        return self.expr
    

    def parse_terms(self) -> list[tuple]:

        seperator_pattern = r"(>=|<=|=)"
        exprs = re.split(seperator_pattern, self.expr)

        self.LHS = exprs[0]
        [self.SEP, self.RHS] = [exprs[1], exprs[2]] if len(exprs) == 3 else [None, None]

        # Regex to capture terms with optional leading signs, coefficients, and variable names
        pattern = r"([+-]?)\s*(\d+)([a-zA-Z]+)"
        return re.findall(pattern, self.LHS)
    

    def extract_terms(self) -> dict[str: float]:
        var_to_coef = {t[2]:float(t[1])*(-1 if t[0] == "-" else 1) for t in self.terms}
        
        match self.SEP:
            case ">=":
                var_to_coef["s"] = 1
            case "=":
                pass

        self.variables = list(var_to_coef.keys())
        self.coefficients = np.array(list(var_to_coef.values()))

        return var_to_coef
    

    def to_vec(self, sort=True) -> np.array:    
        return np.array(self.coefficients) 
    

    def to_row(self, sort=True) -> pd.DataFrame:
        return pd.DataFrame([self.coefficients], columns=self.variables)

# Example usage
equation = "3x + 5y - 2z >= 10"
eq = Equation(equation)
print(eq.to_row())
