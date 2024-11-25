# Prototype Coding Exercise

# Given the definitions shown in code, you are asked to implement Line.deep_copy()  
# to perform a deep copy of the given Line  object. This method should return a copy 
# of a Line that contains copies of its start/end points.

# Note: please do not confuse deep_copy() with __deepcopy__()!

import copy

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start=Point(), end=Point()):
        self.start = start
        self.end = end

    def __str__(self):
        return f"Line starts at {self.start.x}, {self.start.y} and ends at {self.end.x}, {self.end.y}"

    def deep_copy(self):
        line = Line(self.start, self.end)
        return copy.deepcopy(line)

if __name__ == '__main__':
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    line1 = Line(p1, p2)
    line2 = line1.deep_copy()

    print(line1)
    print(line2)
