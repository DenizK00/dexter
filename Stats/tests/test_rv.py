"""
Script Name: test_rv.py
Author: Deniz
Created: 2024-07-09 14:49:28
Description: Testing script for RV
"""


import unittest
from rv import RV
from distribution import Binomial, Poisson

class TestRV(unittest.TestCase):
    def test_expected_value_1(self):
        binom = Binomial(10, 0.4)
        rv = RV(binom)
        self.assertEqual(rv.expected_value, 4)


    def test_expected_value_2(self):
        binom = Binomial(25, 0.6)
        rv = RV(binom)
        self.assertEqual(rv.expected_value, 25*0.6)


    def test_add_binomial(self):
        binom1= Binomial(25, 0.6)
        rv1 = RV(binom1)

        binom2 = Binomial(10, 0.6)
        rv2 = RV(binom2)

        rv_sum = rv1 + rv2

        self.assertIsInstance(rv_sum, RV) # Testing RV Addition
        
        self.assertIsInstance(rv_sum.distribution, Binomial) # Testing distribution
        self.assertEqual(rv_sum.expected_value, 35*0.6) # Testing Binomial sum property

    # def test_add_poisson(self):
    #     poi1 = Poisson(5)
    #     rv1 = RV(poi1)

    #     poi2 = Poisson(8)
    #     rv2 = RV(poi2)
    

if __name__ == '__main__':
    unittest.main()