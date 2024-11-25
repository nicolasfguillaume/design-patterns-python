from abc import ABC


class Expression(ABC):
    pass


class DoubleExpression(Expression):
    def __init__(self, value):
        self.value = value


class AdditionExpression(Expression):
    def __init__(self, left, right):
        self.right = right
        self.left = left


# extract the printing functionality into a separate class (separation of concerns)
class ExpressionPrinter:
    @staticmethod
    def print(e, buffer):
        # /!\ will fail silently on a missing case (for example, if we add a subtraction expression)
        if isinstance(e, DoubleExpression):
            buffer.append(str(e.value))
        elif isinstance(e, AdditionExpression):
            buffer.append('(')
            ExpressionPrinter.print(e.left, buffer)
            buffer.append('+')
            ExpressionPrinter.print(e.right, buffer)
            buffer.append(')')

    # add an attribute to the Expression class (where self refers to the instance of Expression)
    Expression.print = lambda self, b: ExpressionPrinter.print(self, b)


# still breaks OCP because new types require M×N modifications

if __name__ == '__main__':
    # represents 1+(2+3)
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(
            DoubleExpression(2),
            DoubleExpression(3)
        )
    )
    buffer = []

    # ExpressionPrinter.print(e, buffer)

    # IDE might complain here
    e.print(buffer)

    print(''.join(buffer))
