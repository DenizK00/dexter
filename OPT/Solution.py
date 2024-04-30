#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 17:16:19 2024

@author: deniz
"""

import numpy as np
import pyomo.environ as pyo

class Solution:
    def __init__(self, variables:list[str], values:list[float|int]):
        self.variables = variables
        self.values = values
        self.basis = [i for i in range(self.variables) if self.variables[i] > 0]

    @classmethod
    def from_dict(cls, map_dict):
        return cls(list(map_dict.keys()), list(map_dict.values()))
    
    def __str__(self):
        vars_str = ",".join(var for var in self.variables)
        values_str = ",".join(val for val in self.values)
        return f"({vars_str}) = ({values_str})"

    def __getitem__(self, ind:int|str) -> float:
        match ind:
            case isinstance(ind, str):
                return self.variables.index(ind)
            case isinstance(ind, int):
                return self.var_to_coef[self.variables[ind]]

    def feasibility(self):
        # Check the feasibility of solution
        pass

    def optimality(self):
        # Check the optimality of the solution
        pass

    def validate(self):
        # Use feasible
        pass

    def to_numpy_array(self) -> np.array:
        return np.array(self.values)