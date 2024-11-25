# Singleton is a metaclass that inherits from type, which is the default metaclass in Python
class Singleton(type):
    """ Metaclass that creates a Singleton base type when called. """
    # dictionary that will store the single instance of each class that uses Singleton as its metaclass
    _instances = {}

    # In a metaclass, __call__ controls what happens when you try to "call" the class (i.e., create an instance of it)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # This line calls the __call__ method of the superclass (type), which actually creates the new instance of cls
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    def __init__(self):
        print('Loading database')


if __name__ == '__main__':
    d1 = Database()
    d2 = Database()
    print(d1 == d2)
