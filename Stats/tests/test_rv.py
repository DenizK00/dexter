import unittest
from rv import RV
from distribution import Binomial

class TestRV(unittest.TestCase):
    def test_expected_value_1(self):
        binom = Binomial(10, 0.4)
        rv = RV(binom)
        self.assertEqual(rv.expected_value, 4)

    def test_expected_value_2(self):
        binom = Binomial(25, 0.6)
        rv = RV(binom)
        self.assertEqual(rv.expected_value, 25*0.6)

if __name__ == '__main__':
    unittest.main()