class Car:
    def __init__(self, driver):
        self.driver = driver

    def drive(self):
        print(f'Car being driven by {self.driver.name}')


# proxy changes the drive method of the Car class, while having the same interface as before
class CarProxy:
    def __init__(self, driver):
        self.driver = driver
        self.car = Car(driver)

    # expose the same API, with extended functionality
    def drive(self):
        if self.driver.age >= 16:
            self.car.drive()
        else:
            print('Driver too young')


class Driver:
    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == '__main__':
    car = CarProxy(Driver('John', 12))
    car.drive()