# Factory Coding Exercise

# You are given a class called Person. The person has two attributes: id and name .

# Please implement a PersonFactory that has a non-static create_person() method 
# that takes a person's name and return a person initialized with this name and an id.

# The id of the person should be set as a 0-based index of the object created.
# So, the first person the factory makes should have Id=0, second Id=1 and so on.

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"

class PersonFactory:
    # class attribute: shared across all PersonFactory instances
    counter = 0

    def create_person(self, name):
        """takes a person's name and return a person initialized with this name and an id"""
        p = Person(PersonFactory.counter, name)
        PersonFactory.counter += 1
        return p

if __name__ == '__main__':
    p1 = PersonFactory().create_person("Dmitri")
    p2 = PersonFactory().create_person("John")
    print(p1)
    print(p2)
