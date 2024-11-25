# Memento Coding Exercise

# A TokenMachine is in charge of keeping tokens. Each Token is a reference type with 
# a single numerical value. The machine supports adding tokens and, when it does, 
# it returns a memento representing the state of that system at that given time.

# You are asked to fill in the gaps and implement the Memento design pattern for 
# this scenario. Pay close attention to the situation where a token is fed in as 
# a reference and its value is subsequently changed on that reference - you still 
# need to return the correct system snapshot!

import unittest
import copy


class Token:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return f'Token({self.value})'

class Memento(list):
    def __str__(self):
        return f"[{', '.join([str(item) for item in self])}]"

class TokenMachine:
    def __init__(self):
        self.tokens = []

    def add_token_value(self, value):
        return self.add_token(Token(value))

    def add_token(self, token):
        self.tokens.append(token)
        m = Memento(copy.deepcopy(self.tokens))
        return m

    def revert(self, memento):
        self.tokens = memento

    def __str__(self):
        return f"tokens = [{', '.join([str(token) for token in self.tokens])}]\n"


class TestSuite(unittest.TestCase):
    def test_add_tokens(self):
        tm = TokenMachine()
        print(tm)

        m1 = tm.add_token_value(1)
        print(tm)
        print("memento =", m1, "\n")

        m2 = tm.add_token_value(2)
        print(tm)
        print("memento =", m2, "\n")

        m3 = tm.add_token_value(3)
        print(tm)
        print("memento =", m3, "\n")

    def test_revert_token(self):
        tm = TokenMachine()
        print(tm)

        m1 = tm.add_token_value(1)
        print(tm)
        print("memento =", m1, "\n")

        m2 = tm.add_token_value(2)
        print(tm)
        print("memento =", m2, "\n")

        m3 = tm.add_token_value(3)
        print(tm)
        print("memento =", m3, "\n")

        m4 = tm.revert(m2)
        print(tm)

    def test_single_token_1(self):
        tm = TokenMachine()
        m = tm.add_token_value(123)
        tm.add_token_value(456)
        tm.revert(m)
        self.assertEqual(1, len(tm.tokens))
        self.assertEqual(123, tm.tokens[0].value)

    def test_two_tokens(self):
        tm = TokenMachine()
        tm.add_token_value(111)
        m = tm.add_token_value(222)
        tm.add_token_value(333)
        tm.revert(m)
        self.assertEqual(2, len(tm.tokens))
        self.assertEqual(111, tm.tokens[0].value)
        self.assertEqual(222, tm.tokens[1].value)

    def test_fiddled_token(self):
        tm = TokenMachine()
        tm.add_token_value(111)
        m = tm.add_token_value(222)
        tm.add_token_value(333)

        tm.tokens[1].value = 999

        tm.revert(m)
        self.assertEqual(2, len(tm.tokens))
        self.assertEqual(111, tm.tokens[0].value)
        self.assertEqual(222, tm.tokens[1].value)


if __name__ == '__main__':
    unittest.main(exit=False)
