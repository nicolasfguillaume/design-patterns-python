# Strategy Coding Exercise

# Consider the quadratic equation and its canonical solution:

# a*x^2 + b*x + c = 0

# x = (-b +/- sqrt(b^2-4*a*c)) / 2*a

# The part b^2-4*a*c is called the discriminant. Suppose we want to provide an API 
# with two different strategies for calculating the discriminant:

# 1. In OrdinaryDiscriminantStrategy
#    If the discriminant is negative, we return it as-is. 
#    This is OK, since our main API returns Complex numbers anyway.

# 2. In RealDiscriminantStrategy
#    If the discriminant is negative, the return value is NaN (not a number). 
#    NaN propagates throughout the calculation, so the equation solver gives two NaN values. 
#    In Python, you make such a number with float('nan').

# Please implement both of these strategies as well as the equation solver itself. 
# With regards to plus-minus in the formula, please return the + result as the first element 
# and - as the second. Note that the solve() method is expected to return complex values.


from abc import ABC
import unittest
from cmath import sqrt


class DiscriminantStrategy(ABC):
    def calculate_discriminant(self, a, b, c):
        pass


class OrdinaryDiscriminantStrategy(DiscriminantStrategy):
    def calculate_discriminant(self, a, b, c):
        #    If the discriminant is negative, we return it as-is. 
        #    This is OK, since our main API returns Complex numbers anyway.
        return pow(b, 2) - 4 * a * c


class RealDiscriminantStrategy(DiscriminantStrategy):
    def calculate_discriminant(self, a, b, c):
        #    If the discriminant is negative, the return value is NaN (not a number). 
        #    NaN propagates throughout the calculation, so the equation solver gives two NaN values.
        discriminant = pow(b, 2) - 4 * a * c
        if discriminant < 0:
            return float('nan')
        else:
            return discriminant
 

class QuadraticEquationSolver:
    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, a, b, c):
        """ Returns a pair of complex (!) values """
        discriminant = self.strategy.calculate_discriminant(a, b, c)
        print("discriminant =", discriminant)
        # x = (-b +/- sqrt(b ^ 2 - 4 * a * c)) / (2 * a)
        x_plus = (-b + sqrt(discriminant)) / (2 * a)
        x_minus = (-b - sqrt(discriminant)) / (2 * a)
        return [x_plus, x_minus]


class TestSuite(unittest.TestCase):
    def test_OrdinaryDiscriminantStrategy_positive(self):
        strategy = OrdinaryDiscriminantStrategy()
        solver = QuadraticEquationSolver(strategy)
        a = 2
        b = 4
        c = 1
        solution = solver.solve(a, b, c)
        print(solution)

    def test_RealDiscriminantStrategy_positive(self):
        strategy = RealDiscriminantStrategy()
        solver = QuadraticEquationSolver(strategy)
        a = 2
        b = 4
        c = 1
        solution = solver.solve(a, b, c)
        print(solution)

    def test_OrdinaryDiscriminantStrategy_negative(self):
        strategy = OrdinaryDiscriminantStrategy()
        solver = QuadraticEquationSolver(strategy)
        a = 4
        b = 2
        c = 1
        solution = solver.solve(a, b, c)
        print(solution)

    def test_RealDiscriminantStrategy_negative(self):
        strategy = RealDiscriminantStrategy()
        solver = QuadraticEquationSolver(strategy)
        a = 4
        b = 2
        c = 1
        solution = solver.solve(a, b, c)
        print(solution)

if __name__ == '__main__':
    unittest.main(exit=False)
