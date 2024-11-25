# only one instance of the class can exist at any time
def singleton(cls):
    # dictionary to store the instances of the decorated class
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            # if the class has not been instantiated yet, create an instance
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    # returns the get_instance function, which now serves as the constructor for the class
    # (whenever we try to create an instance of the decorated class, get_instance will be called instead)
    return get_instance


@singleton
class Database:
    def __init__(self):
        print('Loading database')


if __name__ == '__main__':
    d1 = Database()
    d2 = Database()
    print(d1 == d2)