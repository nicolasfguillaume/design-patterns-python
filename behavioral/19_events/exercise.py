# Observer Coding Exercise

# Imagine a game where one or more rats can attack a player. Each individual rat has 
# an initial attack value of 1. However, rats attack as a swarm, so each rat's attack value 
# is actually equal to the total number of rats in play.

# Given that a rat enters play through the initializer and leaves play (dies) via 
# its __exit__ method, please implement the Game and Rat classes so that, 
# at any point in the game, the Attack value of a rat is always consistent.


import unittest


class Game:
    # Main idea:
    # when a new rat enters the game:
    #     - he subscribes to the game.rat_enters event
    #     - every subscribed rat gets notified that he entered the game
    #     - other rats have their attack value increases
    #     - other rats notifies the new rat that they exist and his attack value increases
    # when a rat leaves the game:
    #     - every subscribed rat gets notified that he left the game
    #     - other rats have their attack value decreases

    def __init__(self):
        # create a new event for when a rat enters game
        self.rat_enters = Event()
        # create a new event for when other rats are notified
        self.notify_rat = Event()
        # create a new event for when a rat leaves game
        self.rat_dies = Event()


class Rat:
    # rat enters game
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.attack = 1

        # the rat subscribes to each event:
        # add the method self.rat_enters to the game.rat_enters event list
        self.game.rat_enters.append(self.rat_enters)
        # add the methods self.notify_rat to the game.notify_rat event list
        self.game.notify_rat.append(self.notify_rat)
        # add the methods self.rat_dies to the game.rat_dies event list
        self.game.rat_dies.append(self.rat_dies)

        # this fires the game.rat_enters event
        # to notify all subscribed rats that `self` entered the game
        # this will call in a loop: Rat_1.rat_enters(self), Rat_2.rat_enters(self), ...
        self.game.rat_enters(self)

    # entering the context manager
    def __enter__(self):
        return self

    def rat_enters(self, which_rat):
        print(f"[{self.name}.rat_enters] {which_rat.name} (which_rat) entered game -> {self.name} (self) is notified")
        if self != which_rat:
            print(f"[{self.name}.rat_enters] -> different rats -> {self.name}.attack + 1 and notify_rat({which_rat.name}) to increase his attack")
            # if a new rat entered the game, increase the attack value of current rat
            self.attack += 1
            # then fires the game.notify_rat event
            # to notify all subscribed rats that `which_rat` entered the game
            # this will call in a loop: Rat_1.notify_rat(which_rat), Rat_2.notify_rat(which_rat), ...
            self.game.notify_rat(which_rat)  # ... in order to increase which_rat.attack
        else:
            print(f"[{self.name}.rat_enters] -> same rat -> {self.name}.attack unchanged")

    def notify_rat(self, which_rat):
        print(f"  [{self.name}.notify_rat] {which_rat.name} (which_rat) entered game -> {self.name} (self) is notified")
        # every other rats (except self) have their attack value increased
        if self == which_rat:
            print(f"  [{self.name}.notify_rat] -> same rat -> {self.name}.attack + 1")
            self.attack += 1
        else:
            print(f"  [{self.name}.notify_rat] -> different rats -> {self.name}.attack unchanged")

    def rat_dies(self, which_rat):
        print(f"[{self.name}.rat_dies] {which_rat.name} (which_rat) died -> {self.name} (self) is notified -> {self.name}.attack - 1")
        self.attack -= 1

    # exiting the context manager: rat leaves game (dies)
    def __exit__(self, *args):
        # this fires the rat_dies event
        # to notify all subscribed rats that `self` died
        # this will call in a loop: Rat_1.rat_dies(self), Rat_2.rat_dies(self), ...
        self.game.rat_dies(self)


# list of functions that needs to be called when a particular event occurs
class Event(list):
    def __call__(self, *args, **kwargs):
        # for every subscriber in the list
        for item in self:
            # call the subscriber with the arguments
            item(*args, **kwargs)


class TestSuite(unittest.TestCase):
    def test_three_rats_one_dies(self):
        game = Game()
    
        rat = Rat("Rat_1", game)
        self.assertEqual(1, rat.attack)
        print()

        rat2 = Rat("Rat_2", game)
        self.assertEqual(2, rat.attack)
        self.assertEqual(2, rat2.attack)
        print()

        with Rat("Rat_3", game) as rat3:
            self.assertEqual(3, rat.attack)
            self.assertEqual(3, rat2.attack)
            self.assertEqual(3, rat3.attack)
    
        self.assertEqual(2, rat.attack)
        self.assertEqual(2, rat2.attack)


if __name__ == '__main__':
    unittest.main(exit=False)

# OUTPUT:

# [Rat_1.rat_enters] Rat_1 (which_rat) entered game -> Rat_1 (self) is notified
# [Rat_1.rat_enters] -> same rat -> Rat_1.attack unchanged

# [Rat_1.rat_enters] Rat_2 (which_rat) entered game -> Rat_1 (self) is notified
# [Rat_1.rat_enters] -> different rats -> Rat_1.attack + 1 and notify_rat(Rat_2) to increase his attack
#   [Rat_1.notify_rat] Rat_2 (which_rat) entered game -> Rat_1 (self) is notified
#   [Rat_1.notify_rat] -> different rats -> Rat_1.attack unchanged
#   [Rat_2.notify_rat] Rat_2 (which_rat) entered game -> Rat_2 (self) is notified
#   [Rat_2.notify_rat] -> same rat -> Rat_2.attack + 1
# [Rat_2.rat_enters] Rat_2 (which_rat) entered game -> Rat_2 (self) is notified
# [Rat_2.rat_enters] -> same rat -> Rat_2.attack unchanged

# [Rat_1.rat_enters] Rat_3 (which_rat) entered game -> Rat_1 (self) is notified
# [Rat_1.rat_enters] -> different rats -> Rat_1.attack + 1 and notify_rat(Rat_3) to increase his attack
#   [Rat_1.notify_rat] Rat_3 (which_rat) entered game -> Rat_1 (self) is notified
#   [Rat_1.notify_rat] -> different rats -> Rat_1.attack unchanged
#   [Rat_2.notify_rat] Rat_3 (which_rat) entered game -> Rat_2 (self) is notified
#   [Rat_2.notify_rat] -> different rats -> Rat_2.attack unchanged
#   [Rat_3.notify_rat] Rat_3 (which_rat) entered game -> Rat_3 (self) is notified
#   [Rat_3.notify_rat] -> same rat -> Rat_3.attack + 1
# [Rat_2.rat_enters] Rat_3 (which_rat) entered game -> Rat_2 (self) is notified
# [Rat_2.rat_enters] -> different rats -> Rat_2.attack + 1 and notify_rat(Rat_3) to increase his attack
#   [Rat_1.notify_rat] Rat_3 (which_rat) entered game -> Rat_1 (self) is notified
#   [Rat_1.notify_rat] -> different rats -> Rat_1.attack unchanged
#   [Rat_2.notify_rat] Rat_3 (which_rat) entered game -> Rat_2 (self) is notified
#   [Rat_2.notify_rat] -> different rats -> Rat_2.attack unchanged
#   [Rat_3.notify_rat] Rat_3 (which_rat) entered game -> Rat_3 (self) is notified
#   [Rat_3.notify_rat] -> same rat -> Rat_3.attack + 1
# [Rat_3.rat_enters] Rat_3 (which_rat) entered game -> Rat_3 (self) is notified
# [Rat_3.rat_enters] -> same rat -> Rat_3.attack unchanged
# [Rat_1.rat_dies] Rat_3 (which_rat) died -> Rat_1 (self) is notified -> Rat_1.attack - 1
# [Rat_2.rat_dies] Rat_3 (which_rat) died -> Rat_2 (self) is notified -> Rat_2.attack - 1
# [Rat_3.rat_dies] Rat_3 (which_rat) died -> Rat_3 (self) is notified -> Rat_3.attack - 1
