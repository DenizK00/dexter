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

    def __init__(self, expr: str, name=""):
        self.name = name
        self.expr = expr
        self.validate_expression()
        self.terms = self.parse_terms()
        self.var_to_coef = self.extract_terms() #ADD  


    def __str__(self) -> str:
        return self.expr
    
    def __getitem__(self, index:int|str) -> float:
        match index:
            case isinstance(index, str):
                return self.var_to_coef[index]
            case isinstance(index, int):
                return self.var_to_coef[self.variables[index]]

    def __repr__(self) -> str:
        if self.name:
            repr = f"Equation({self.expr!r}, name={self.name})"
        else:
            repr = f"Equation({self.expr!r})"
        return repr


    def validate_expression(self):
        seperator_pattern = r"(>=|<=|=)"
        exprs = re.split(seperator_pattern, self.expr)

        if len(exprs) != 3:
            self.LHS = exprs[0] ### check
        else: 
            self.LHS, self.SEP, self.RHS = exprs
            
            if self.SEP not in ["<=", ">=", "="]:
                raise ValueError("Unsupported operator. Only <=, >=, and = are supported.")

            # THINK ABOUT THIS ONE
            # self.SEP = "==" if self.SEP == "=" else self.SEP
        
        return


    def parse_terms(self) -> list[tuple]:
        # Regex to capture terms with optional leading signs, coefficients, and variable names
        # Pattern without exponent: r"([+-]?)\s*(\d+)?([a-zA-Z]+)"
        # Pattern with exponents: r"([+-]?)\s*(\d+)?([a-zA-Z]+)(\^(\d+))?""

        pattern = r"([+-]?)\s*(\d+)?([a-zA-Z]+)"
        return re.findall(pattern, self.LHS)


    def extract_terms(self) -> dict[str : float]:
        var_to_coef = {}
        for t in self.terms:
            try:
                var_to_coef[t[2]] = float(t[1])*(-1 if t[0] == "-" else 1)
            except ValueError:
                var_to_coef[t[2]] = -1 if t[0] == "-" else 1

        
        self.variables = list(var_to_coef.keys())
        self.coefficients = np.array(list(var_to_coef.values()))

        return var_to_coef
    

    def __copy__(self):
        return copy.deepcopy(self)

         
    def add_slack(self):

        # Maybe create a new instance of Equation with the changed expression
        match self.SEP:
            case ">=":
                slack_expr = f"{self.LHS}- s ={self.RHS}"
            case "<=": 
                slack_expr = f"{self.LHS}+ s ={self.RHS}"
            case _:
                raise InvalidForm
        
        slack_eq = Equation(slack_expr)

        # Might be necessary afterwards
        # if self.RHS:
        #     copy_eq.var_to_coef["="] = self.RHS

        return slack_eq


    ## Maybe add triv for trivial form where RHS = 0
    # def triv_form(self):

    def to_numpy_array(self) -> np.array:
        return np.array(self.coefficients)


    def to_pandas_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self.coefficients], columns=self.variables, index=[self.name + ":"])