# Chain of Responsibility Coding Exercise

# You are given a game scenario with classes Goblin and GoblinKing. Please implement the following rules:

# A goblin has base 1 attack/1 defense (1/1), a goblin king is 3/3.

# When the Goblin King is in play, every other goblin gets +1 Attack.

# Goblins get +1 to Defense for every other Goblin in play (a GoblinKing is a Goblin!).

# Example:

# Suppose you have 3 ordinary goblins in play. Each one is a 1/3 (1/1 + 0/2 defense bonus).

# A goblin king comes into play. Now every goblin is a 2/4 (1/1 + 0/3 defense bonus from each other + 1/0 from goblin king)

# The state of all the goblins has to be consistent as goblins are added and removed from the game.

# Note: creature removal (unsubscription) does not need to be implemented.

from enum import Enum
from abc import ABC
import unittest


class Creature(ABC):
    def __init__(self, game, attack, defense):
        self.initial_defense = defense
        self.initial_attack = attack
        self.game = game

    @property
    def attack(self):
        pass

    @property
    def defense(self):
        pass

    def query(self, source, query):
        pass


class Goblin(Creature):
    def __init__(self, game, attack=1, defense=1):
        super().__init__(game, attack, defense)

    @property
    def attack(self):
        q = Query(self.initial_attack, WhatToQuery.ATTACK)
        for creature in self.game.creatures:
            creature.query(source=self, query=q)
        return q.value

    @property
    def defense(self):
        q = Query(self.initial_defense, WhatToQuery.DEFENSE)
        for creature in self.game.creatures:
            creature.query(source=self, query=q)
        return q.value

    def query(self, source, query):
        # Goblins get +1 to Defense for every other Goblin in play (a GoblinKing is a Goblin!)
        if self != source and query.what_to_query == WhatToQuery.DEFENSE:
            query.value += 1


class GoblinKing(Goblin):
    def __init__(self, game):
        super().__init__(game, attack=3, defense=3)

    def query(self, source, query):
        # When the Goblin King is in play, every other goblin gets +1 Attack
        if self != source and query.what_to_query == WhatToQuery.ATTACK:
            query.value += 1
        else:
            super().query(source, query)


class WhatToQuery(Enum):
    ATTACK = 1
    DEFENSE = 2


class Query:
    def __init__(self, initial_value, what_to_query):
        self.value = initial_value
        self.what_to_query = what_to_query


class Game:
    def __init__(self):
        self.creatures = []


class TestSuite(unittest.TestCase):
    def test_one_goblin(self):
        game = Game()
        goblin = Goblin(game)
        game.creatures.append(goblin)
 
        self.assertEqual(1, goblin.attack)
        self.assertEqual(1, goblin.defense)

    def test_three_goblins(self):
        game = Game()
        goblin_1 = Goblin(game)
        game.creatures.append(goblin_1)
        goblin_2 = Goblin(game)
        game.creatures.append(goblin_2)
        goblin_3 = Goblin(game)
        game.creatures.append(goblin_3)
 
        # Goblins get +1 to Defense for every other Goblin in play (a GoblinKing is a Goblin!).
        self.assertEqual(1, goblin_1.attack)
        self.assertEqual(1+1+1, goblin_1.defense)
        self.assertEqual(1, goblin_2.attack)
        self.assertEqual(1+1+1, goblin_2.defense)
        self.assertEqual(1, goblin_3.attack)
        self.assertEqual(1+1+1, goblin_3.defense)

        # A goblin king comes into play.
        goblin_king = GoblinKing(game)
        game.creatures.append(goblin_king)

        # When the Goblin King is in play, every other goblin gets +1 Attack.
        self.assertEqual(1+1, goblin_1.attack)
        # Goblins get +1 to Defense for every other Goblin in play (a GoblinKing is a Goblin!).
        self.assertEqual(1+1+1+1, goblin_1.defense)
        self.assertEqual(1+1, goblin_2.attack)
        self.assertEqual(1+1+1+1, goblin_2.defense)
        self.assertEqual(1+1, goblin_3.attack)
        self.assertEqual(1+1+1+1, goblin_3.defense)

        self.assertEqual(3, goblin_king.attack)
        self.assertEqual(3+1+1+1, goblin_king.defense)


if __name__ == '__main__':
    unittest.main(exit=False)
