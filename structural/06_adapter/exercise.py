# Adapter Coding Exercise

# You are given a class called Square and a function calculate_area() which calculates the area of a given rectangle.

# In order to use Square in calculate_area, instead of augmenting it with width/height members, 
# please implement the SquareToRectangleAdapter class. This adapter takes a square and adapts it 
# in such a way that it can be used as an argument to calculate_area().

class Square:
    def __init__(self, side=0):
        self.side = side

def calculate_area(rc):
    """Calculate the area of a given rectangle"""
    print(rc.width, rc.height)
    return rc.width * rc.height


class SquareToRectangleAdapter:
    # SquareToRectangleAdapter exposes a width and height attribute based on the Square’s side, 
    # allowing it to act as a rectangle while still maintaining the connection to the original Square instance.
    def __init__(self, square):
        self.square = square

    @property
    def width(self):
        # maintaining the connection to the original Square instance
        return self.square.side
    
    @property
    def height(self):
        # maintaining the connection to the original Square instance
        return self.square.side

# This does not work, because it does not maintain the connection to the original Square instance
# class SquareToRectangleAdapter:
#     def __init__(self, square):
#         self.width = square.side
#         self.height = square.side

if __name__ == '__main__':
    square = Square(5)
    rectangle = SquareToRectangleAdapter(square)

    area = calculate_area(rectangle)
    assert area == 25
    print(area)

    square.side = 10
    # The reason a change to an instance of Square affects the corresponding SquareToRectangleAdapter instance
    # is due to *object references*. In Python, when you pass an object to another class, 
    # you are not creating a copy of the object; instead, you are passing a reference to the same object in memory.
    print(rectangle.width, rectangle.height)
    area = calculate_area(rectangle)
    # assert area == square.side * square.side
    print(area)
