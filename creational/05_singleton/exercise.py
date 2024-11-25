# Singleton Coding Exercise

# Since implementing a singleton is easy, you have a different challenge: write a function called is_singleton(). 
# This method takes a factory method that returns an object and it's up to you to determine whether or not that 
# object is a singleton instance.

import random

def is_singleton(factory) -> bool:
    # todo: call factory() and return true or false
    # depending on whether the factory makes a singleton or not
    obj1 = factory()
    obj2 = factory()
    return obj1 == obj2


# copied from singleton_decorator.py
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class NonSingletonDatabase:
    def __init__(self):
        print('Loading database', random.randint(1, 101))

@singleton
class SingletonDatabase:
    def __init__(self):
        print('Loading database', random.randint(1, 101))


class DatabaseFactory:
    @staticmethod
    def new_non_singleton_database():
        return NonSingletonDatabase()
    
    @staticmethod
    def new_singleton_database():
        return SingletonDatabase()


if __name__ == '__main__':
    dbf = DatabaseFactory()

    print('Testing Non-singleton database')
    assert not is_singleton(dbf.new_non_singleton_database)
    print('Testing Singleton database')
    assert is_singleton(dbf.new_singleton_database)
