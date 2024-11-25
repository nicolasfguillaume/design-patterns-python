# Mediator Coding Exercise

# Our system has any number of instances of Participant  classes. Each Participant has a value 
# integer attribute, initially zero.

# A participant can say() a particular value, which is broadcast to all other participants. 
# At this point in time, every other participant is obliged to increase their value  by the 
# value being broadcast.

# Example:

# Two participants start with values 0 and 0 respectively

# Participant 1 broadcasts the value 3. We now have Participant 1 value = 0, Participant 2 value = 3

# Participant 2 broadcasts the value 2. We now have Participant 1 value = 2, Participant 2 value = 3

import unittest


class Participant:
    def __init__(self, mediator):
        self.value = 0
        self.mediator = mediator
        self.mediator.participants.append(self)

    def say(self, value):
        self.mediator.broadcast(self, value)

    def receive(self, value):
        self.value += value


class Mediator:
    def __init__(self):
        self.participants = []

    def broadcast(self, participant, value):
        for p in self.participants:
            if p != participant:
                p.receive(value)


class TestSuite(unittest.TestCase):
    def test_1(self):
        mediator = Mediator()
        p1 = Participant(mediator)
        p2 = Participant(mediator)

        # Participant 1 broadcasts the value 3. We now have Participant 1 value = 0, Participant 2 value = 3
        p1.say(3)
        self.assertEqual(p1.value, 0)
        self.assertEqual(p2.value, 3)

        # Participant 2 broadcasts the value 2. We now have Participant 1 value = 2, Participant 2 value = 3
        p2.say(2)
        self.assertEqual(p1.value, 2)
        self.assertEqual(p2.value, 3)


if __name__ == '__main__':
    unittest.main(exit=False)
