"""
Script Name: test_eq.py
Author: Deniz
Created: 2024-08-18 20:00:09
Description: Script Description
"""


import unittest
from equation import Equation

class TestRV(unittest.TestCase):
    def test_parsing_1(self):
        eq = Equation("2*x + 5*y >= 5", name="example")

        """Check initialization"""
        assert(isinstance(eq, Equation))
        assert(eq.name == "example")

        """Check variable and coefficient read"""
        assert(eq.var_to_coef == {"x":2, "y":5})

    



if __name__ == '__main__':
    unittest.main()