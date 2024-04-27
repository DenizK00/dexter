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

class InvalidForm(Exception): pass

class Equation:
    def __init__(self, expr: str, name=None):
        self.name = name
        self.expr = expr
        self.validate_expression()
        self.terms = self.parse_terms()
        self.var_to_coef = self.extract_terms()


    def __str__(self) -> str:
        return self.expr

    def __repr__(self) -> str:
        return f"Equation({self.expr!r})"

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


    def extract_terms(self) -> dict[str: float]:
        var_to_coef = {t[2]:float(t[1])*(-1 if t[0] == "-" else 1) for t in self.terms}
        
        self.variables = list(var_to_coef.keys())
        self.coefficients = np.array(list(var_to_coef.values()))

        return var_to_coef

         
    def add_slack(self):

        # Maybe create a new instance of Equation with the changed expression
        match self.SEP:
            case ">=":
                slack_coef = 1
                new_expr = f"{self.LHS}- s ={self.RHS}"
            case "<=": 
                slack_coef = -1
                new_expr = f"{self.LHS}+ s ={self.RHS}"
            case _:
                raise InvalidForm
        
        new_eq = Equation(new_expr)

        # Might be necessary
        # if self.RHS:
        #     copy_eq.var_to_coef["="] = self.RHS

        return copy_eq


    def to_numpy_array(self) -> np.array:
        return np.array(self.coefficients)


    def to_pandas_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self.coefficients], columns=self.variables, index=[self.name + ":"])
    
    