#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 19:46:22 2024

@author: deniz
"""

import sympy as sp
import pandas as pd
import numpy as np

class InvalidForm(Exception): pass

class Equation:
    def __init__(self, expr: str, name=""):
        self.name = name
        self.expr = sp.sympify(expr, evaluate=False)  # Convert the string expression to a SymPy expression
        self.LHS, self.RHS = self.validate_expression(self.expr)
        self.var_to_coef = self.extract_terms()

    def __str__(self) -> str:
        return self.expr
    
    def __getitem__(self, index: int | str) -> float:
        if isinstance(index, str):
            return self.var_to_coef.get(index, 0)
        elif isinstance(index, int):
            return self.var_to_coef.get(self.variables[index], 0)

    def __repr__(self) -> str:
        return f"Equation('{self.expr}', name={self.name})" if self.name else f"Equation('{self.expr}')"

    def validate_expression(self, expr):
        # Decompose the expression into LHS and RHS using equality or inequality
        relations = [sp.Eq, sp.Le, sp.Ge]
        for rel in relations:
            if isinstance(expr, rel):
                return expr.lhs, expr.rhs
            
        raise ValueError("Unsupported operator. Only <=, >=, and = are supported.")

    def extract_terms(self) -> dict[str, float]:
        # Extract terms and their coefficients from the LHS
        lhs_poly = sp.Poly(self.LHS)
        var_to_coef = {str(var): lhs_poly.coeff_monomial(var) for var in lhs_poly.gens}
        self.variables = list(var_to_coef.keys())
        self.coefficients = np.array(list(var_to_coef.values()))
        return var_to_coef

    def __copy__(self):
        return type(self)(str(self.expr), self.name)

    def add_slack(self):
        # add a slack variable
        slack_var = sp.Symbol('slack')

        if isinstance(self.expr, sp.Ge):  # Greater than or equal
            new_expr = sp.Eq(self.LHS - slack_var, self.RHS)

        elif isinstance(self.expr, sp.Le):  # Less than or equal
            new_expr = sp.Eq(self.LHS + slack_var, self.RHS)

        else:
            raise InvalidForm("Invalid equation form for adding slack.")
        
        return Equation(str(new_expr))

    def to_numpy_array(self) -> np.array:
        return self.coefficients

    def to_pandas_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self.coefficients], columns=self.variables, index=[self.name + ":"] if self.name else [""])
