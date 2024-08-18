"""
Script Name: test_eq.py
Author: Deniz
Created: 2024-08-18 20:00:09
Description: Script Description
"""


import unittest
from equation import Equation

class TestRV(unittest.TestCase):
    def test_expected_value_1(self):
        Equation("2x + 5y = 5")

if __name__ == '__main__':
    unittest.main()