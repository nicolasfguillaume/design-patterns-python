# list of functions that needs to be called when a particular event occurs
class Event(list):
    def __call__(self, *args, **kwargs):
        # for every subscriber in the list
        for item in self:
            # call the subscriber with the arguments
            item(*args, **kwargs)


class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        # create a new event for when a person falls ill
        # other classes can subscribe to this event and get notified when it occurs
        self.falls_ill = Event()

    def catch_a_cold(self):
        # this fires the event
        self.falls_ill(self.name, self.address)


def call_doctor(name, address):
    print(f'A doctor has been called to {address}')


if __name__ == '__main__':
    person = Person('Sherlock', '221B Baker St')

    # add a new subscriber (lambda) to the falls_ill event
    # so when a person falls ill, print that the person is ill
    person.falls_ill.append(lambda name, addr: print(f'{name} is ill'))

    # add a new subscriber (call_doctor) to the falls_ill event
    # so when a person falls ill, call the doctor
    person.falls_ill.append(call_doctor)

    person.catch_a_cold()

    # and you can remove subscriptions too
    person.falls_ill.remove(call_doctor)
    person.catch_a_cold()