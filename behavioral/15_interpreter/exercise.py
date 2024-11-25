# Interpreter Coding Exercise

# You are asked to write an expression processor for simple numeric expressions with the following constraints:

# Expressions use integral values (e.g., '13' ), single-letter variables defined in Variables, as well as + and - operators only

# There is no need to support braces or any other operations

# If a variable is not found in variables  (or if we encounter a variable with >1 letter, e.g. ab), the evaluator returns 0 (zero)

# In case of any parsing failure, evaluator returns 0


import unittest
from enum import Enum


class ExpressionProcessor:
    def __init__(self):
        self.variables = {}

    def calculate(self, expression):    
        tokens = self.lex(expression)
        print(' '.join(map(str, tokens)))

        parsed = self.parse(tokens)
        print(f'{input} = {parsed.value}')

        return parsed.value

    @staticmethod
    def lex(input):
        result = []

        i = 0
        while i < len(input):
            if input[i] == '+':
                result.append(Token(Token.Type.PLUS, '+'))
            elif input[i] == '-':
                result.append(Token(Token.Type.MINUS, '-'))
            elif input[i].isalpha():
                # initialize a list of characters with the current character
                characters = [input[i]]
                # scanning characters from the next character to the end of the input
                for j in range(i + 1, len(input)):
                    if input[j].isalpha():
                        characters.append(input[j])
                        i += 1
                    else:
                        result.append(Token(Token.Type.VARIABLE, ''.join(characters)))
                        break
                if i + 1 == len(input):
                    result.append(Token(Token.Type.VARIABLE, ''.join(characters)))
            # must be a number
            else:
                # initialize a list of digits with the current character
                digits = [input[i]]
                # scanning characters from the next character to the end of the input
                print(f'input[i={i}]:', input[i])
                for j in range(i + 1, len(input)):
                    print(f'input[j={j}]:', input[j])
                    if input[j].isdigit():
                        digits.append(input[j])
                        i += 1
                    else:
                        result.append(Token(Token.Type.INTEGER, ''.join(digits)))
                        break
                if i + 1 == len(input):
                    result.append(Token(Token.Type.INTEGER, ''.join(digits)))
            i += 1

        return result

    def parse(self, tokens):
        result = BinaryOperation()
        have_lhs = False
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if result.left and result.right and result.type:
                result.left = Integer(result.value)
                result.right = None
                result.type = None

            print(f'token.text: {token.text}')
            print(f'result: {vars(result)}')

            if token.type == Token.Type.VARIABLE:
                variable = Integer(self.variables.get(token.text, None))
                # If a variable is not found in variables 
                # (or if we encounter a variable with >1 letter, e.g. ab), the evaluator returns 0 (zero)
                if variable is None or len(token.text) > 1:
                    result.right = None
                    result.type = None
                    return result
                if not have_lhs:
                    result.left = variable
                    have_lhs = True
                else:
                    result.right = variable
            elif token.type == Token.Type.INTEGER:
                integer = Integer(int(token.text))
                if not have_lhs:
                    result.left = integer
                    have_lhs = True
                else:
                    result.right = integer
            elif token.type == Token.Type.PLUS:
                result.type = BinaryOperation.Type.ADDITION
            elif token.type == Token.Type.MINUS:
                result.type = BinaryOperation.Type.SUBTRACTION
            i += 1
        return result


class Token:
    class Type(Enum):
        INTEGER = 0
        PLUS = 1
        MINUS = 2
        VARIABLE = 3

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        return f'`{self.text}`'


class Integer:
    def __init__(self, value):
        self.value = value


class BinaryOperation:
    class Type(Enum):
        ADDITION = 0
        SUBTRACTION = 1

    def __init__(self):
        self.type = None
        self.left = None
        self.right = None

    @property
    def value(self):
        if self.type == self.Type.ADDITION:
            return self.left.value + self.right.value
        elif self.type == self.Type.SUBTRACTION:
            return self.left.value - self.right.value
        elif self.left is None or self.right is None:
            return 0


class TestSuite(unittest.TestCase):
    def test_exercise_1(self):
        ep = ExpressionProcessor()
        self.assertEqual(6, ep.calculate("1+2+3"))
        self.assertEqual(37, ep.calculate("1+2+34"))

    def test_exercise_2(self):
        ep = ExpressionProcessor()
        self.assertEqual(0, ep.calculate("1+2+xy"))

    def test_exercise_3(self):
        ep = ExpressionProcessor()
        ep.variables = {"x": 3}
        self.assertEqual(5, ep.calculate("10-2-x"))


if __name__ == '__main__':
    unittest.main(exit=False)
