# Builder Coding Exercise

# You are asked to implement the Builder design pattern for rendering simple chunks of code.

# Sample use of the builder you are asked to create:

# cb = CodeBuilder('Person').add_field('name', '""') \
#                           .add_field('age', '0')
# print(cb)

# The expected output of the above code is:

# class Person:
#   def __init__(self):
#     self.name = ""
#     self.age = 0

# Please observe the same placement of spaces and indentation.


class Field:
    def __init__(self, name='', value=''):
        self.name = name
        self.value = value

    def __str__(self):
        return f'    self.{self.name} = {self.value}'


class Class:
    def __init__(self, name=''):
        self.name = name
        self.fields = []

    def __str__(self):
        lines = []

        lines.append(f'class {self.name}:')
    
        if self.fields:
            lines.append(f'  def __init__(self):')
            for f in self.fields:
                lines.append(str(f))
        else:
            lines.append(f'  pass')

        return '\n'.join(lines)


class CodeBuilder:
    __class = Class()
    
    def __init__(self, class_name):
        self.class_name = class_name
        self.__class.name = class_name

    def add_field(self, field_name, field_value):
        self.__class.fields.append(Field(field_name, field_value))
        return self

    def __str__(self):
        return str(self.__class)


if __name__ == '__main__':
    cb = CodeBuilder('Foo')
    print(cb)
            
    cb = CodeBuilder('Person') \
        .add_field('name', '""') \
        .add_field('age', '0')
    print(cb)
