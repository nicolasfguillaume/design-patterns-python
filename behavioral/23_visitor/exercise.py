# Visitor Coding Exercise

# You are asked to implement a visitor called ExpressionPrinter for printing different 
# mathematical expressions. The range of expressions covers addition and multiplication 
# - please put round brackets around addition operations (but not multiplication ones)! 
# Also, please avoid any blank spaces in output.

# Example:

# Input: AdditionExpression(Value(2), Value(3)) 

# Output: (2+3) 

# taken from https://tavianator.com/the-visitor-pattern-in-python/

import unittest
from abc import ABC


def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods = {}


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    key = (_qualname(type(self)), type(arg))
    if not key in _methods:
        raise Exception('Key % not found' % key)
    method = _methods[key]
    return method(self, arg)


# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator

# ↑↑↑ LIBRARY CODE ↑↑↑

class Value:
    def __init__(self, value):
        self.value = value


class AdditionExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left


class MultiplicationExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left


class ExpressionPrinter:
    def __init__(self):
        self.buffer = []

    def __str__(self):
        return "".join(self.buffer)

    @visitor(Value)
    def visit(self, obj):
        self.buffer.append(str(obj.value))

    @visitor(AdditionExpression)
    def visit(self, obj):
        self.buffer.append("(")
        self.visit(obj.left)
        self.buffer.append("+")
        self.visit(obj.right)
        self.buffer.append(")")

    @visitor(MultiplicationExpression)
    def visit(self, obj):
        self.visit(obj.left)
        self.buffer.append("*")
        self.visit(obj.right)


class Evaluate(unittest.TestCase):
    def test_simple_addition(self):
        simple = AdditionExpression(Value(2), Value(3))
        ep = ExpressionPrinter()
        ep.visit(simple)
        self.assertEqual("(2+3)", str(ep))

    def test_simple_multiplication(self):
        simple = MultiplicationExpression(Value(2), Value(3))
        ep = ExpressionPrinter()
        ep.visit(simple)
        self.assertEqual("2*3", str(ep))

    def test_simple_addition_multiplication(self):
        expr = AdditionExpression(
            Value(2),
            MultiplicationExpression(
                Value(3),
                Value(4)
            )
        )
        ep = ExpressionPrinter()
        ep.visit(expr)
        self.assertEqual("(2+3*4)", str(ep))

    def test_simple_multiplication_addition(self):
        expr = MultiplicationExpression(
            Value(2),
            AdditionExpression(
                Value(3),
                Value(4)
            )
        )
        ep = ExpressionPrinter()
        ep.visit(expr)
        self.assertEqual("2*(3+4)", str(ep))

if __name__ == '__main__':
    unittest.main(exit=False)
