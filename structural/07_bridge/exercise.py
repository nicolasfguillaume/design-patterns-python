# Bridge Coding Exercise

# You are given an example of an inheritance hierarchy which results in Cartesian-product duplication.

# Please refactor this hierarchy, giving the base class Shape a constructor that takes an interface Renderer defined as

# class Renderer(ABC):
#     @property
#     def what_to_render_as(self):
#         return None

# as well as VectorRenderer  and RasterRenderer  classes. Each inheritor of the Shape abstract class should have a 
# constructor that takes a Renderer such that, subsequently, each constructed object's __str__()  operates correctly, 
# for example:
# str(Triangle(RasterRenderer())  # returns "Drawing Triangle as pixels" 

# existing hierarchy:
# shape
# - triangle
#     - vector triangle
#     - raster triangle
# - square
#     - vector square
#     - raster square

# new hierarchy:
# shape
#     - triangle
#     - square
# renderer
#     - vector renderer
#     - raster renderer

from abc import ABC


class Shape:
    def __init__(self, renderer):
        self.renderer = renderer
    
    def __str__(self):
        return self.renderer.what_to_render_as


class Triangle(Shape):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.name = 'Triangle'
        self.renderer.name = self.name


class Square(Shape):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.name = 'Square'
        self.renderer.name = self.name


class Renderer(ABC):
    @property
    def what_to_render_as(self):
        return None


class VectorRenderer(Renderer):
    @property
    def what_to_render_as(self):
        return f'Drawing {self.name} as lines'


class RasterRenderer(Renderer):
    @property
    def what_to_render_as(self):
        return f'Drawing {self.name} as pixels'


if __name__ == '__main__':
    print(Triangle(RasterRenderer()))  # returns "Drawing Triangle as pixels" 
    print(Square(VectorRenderer()))    # returns "Drawing Square as lines"
