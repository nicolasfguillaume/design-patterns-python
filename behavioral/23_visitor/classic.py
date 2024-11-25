# taken from https://tavianator.com/the-visitor-pattern-in-python/


def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods = {}
# every time we use the @visitor decorator, we add a new method to this dictionary:
# {
# ('__main__.ExpressionPrinter', <class '__main__.DoubleExpression'>): <function ExpressionPrinter.visit at 0x100c81d00>, 
# ('__main__.ExpressionPrinter', <class '__main__.AdditionExpression'>): <function ExpressionPrinter.visit at 0x100c81e40>
# }


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    # Retrieve the method from the _methods dictionary
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg)


# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        # Registers a visitor method for a specific argument type
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator


# ↑↑↑ LIBRARY CODE ↑↑↑

class DoubleExpression:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit(self)


class AdditionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        visitor.visit(self)


class ExpressionPrinter:
    def __init__(self):
        # now the buffer is an attribute of the class
        self.buffer = []

    # implementation of the Double Dispatch

    # visit method for the DoubleExpression type
    @visitor(DoubleExpression)
    def visit(self, de):
        self.buffer.append(str(de.value))

    # visit method for the AdditionExpression type
    @visitor(AdditionExpression)
    def visit(self, ae):
        self.buffer.append('(')
        ae.left.accept(self)
        self.buffer.append('+')
        ae.right.accept(self)
        self.buffer.append(')')

    def __str__(self):
        return ''.join(self.buffer)


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
    printer = ExpressionPrinter()
    printer.visit(e)
    print(printer)
    print(_methods)
