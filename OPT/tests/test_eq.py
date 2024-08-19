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
        self.assertIsInstance(eq, Equation)
        self.assertEqual(eq.name, "example")

        """Check variable and coefficient read"""

        self.assertDictEqual(eq.var_to_coef, {"x": 2, "y": 5})

    def test_parsing_2(self):
        import numpy as np

        eq_str = ""
        rand_coefs = np.linspace(1, 20, 10)
        i = 1
        for coef in rand_coefs:
            eq_str += f"{round(coef)}*x_{i} + "
            i+=1
        
        self.assertDictEqual(eq.var_to_coef, {"x":3, "y":7, "z":9})

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            Equation("x === 5")


if __name__ == '__main__':
    unittest.main()