# Template Method Coding Exercise

# Imagine a typical collectible card game which has cards representing creatures. 
# Each creature has two values: Attack and Health. Creatures can fight each other, 
# dealing their Attack damage, thereby reducing their opponent's health.

# The class CardGame implements the logic for two creatures fighting one another. 
# However, the exact mechanics of how damage is dealt is different:

# - TemporaryCardDamage : In some games (e.g., Magic: the Gathering), unless the creature 
#   has been killed, its health returns to the original value at the end of combat.

# - PermanentCardDamage : In other games (e.g., Hearthstone), health damage persists.

# You are asked to implement classes TemporaryCardDamageGame and PermanentCardDamageGame 
# that would allow us to simulate combat between creatures.

# Some examples:

# - With temporary damage, creatures 1/2 and 1/3 can never kill one another. 
#   With permanent damage, second creature will win after 2 rounds of combat.

# - With either temporary or permanent damage, two 2/2 creatures kill one another.


import unittest
from abc import ABC


class Creature:
    def __init__(self, attack, health):
        self.health = health
        self.attack = attack


class CardGame(ABC):
    def __init__(self, creatures):
        self.creatures = creatures

    # return -1 if both creatures alive or both dead after combat
    # otherwise, return the _index_ of winning creature
    def combat(self, c1_index, c2_index):
        c1 = self.creatures[c1_index]
        c2 = self.creatures[c2_index]

        self.hit(c1, c2)
        self.hit(c2, c1)

        is_c1_alive = c1.health > 0
        is_c2_alive = c2.health > 0

        if (is_c1_alive and is_c2_alive) or (not is_c1_alive and not is_c2_alive):
            return -1
        elif is_c1_alive:
            return c1_index
        elif is_c2_alive:
            return c2_index     

    def hit(self, attacker, defender):
        pass


class TemporaryDamageCardGame(CardGame):
    def hit(self, attacker, defender):
        # unless the creature has been killed, its health returns to the 
        # original value at the end of combat.
        defender_initial_health = defender.health
        defender.health -= attacker.attack
        if defender.health > 0:
            defender.health = defender_initial_health


class PermanentDamageCardGame(CardGame):
    def hit(self, attacker, defender):
        # health damage persists
        defender.health -= attacker.attack


class TestSuite(unittest.TestCase):
    def test_TemporaryDamageCardGame_impasse(self):
        c1 = Creature(1, 2)
        c2 = Creature(1, 3)
        game = TemporaryDamageCardGame([c1, c2])
        winner_index = game.combat(0, 1)
        # no winner: they can never kill one another
        print(winner_index)

    def test_PermanentDamageCardGame_two_rounds(self):
        c1 = Creature(1, 2)
        c2 = Creature(1, 3)
        game = PermanentDamageCardGame([c1, c2])
        _ = game.combat(0, 1)  # first round
        winner_index = game.combat(0, 1)  # second round
        # second creature will win after 2 rounds of combat
        self.assertEqual(winner_index, 1)
        print(c1.health)
        # permanent damage: health damage persists to 0
        self.assertEqual(c1.health, 0)

    def test_TemporaryDamageCardGame_mutual_death(self):
        c1 = Creature(2, 2)
        c2 = Creature(2, 2)
        game = TemporaryDamageCardGame([c1, c2])
        winner_index = game.combat(0, 1)
        # no winner: creatures kill one another
        self.assertEqual(winner_index, -1)
        # permanent damage: health returns to initial state
        self.assertEqual(c1.health, 0)

    def test_PermanentDamageCardGame_mutual_death(self):
        c1 = Creature(2, 2)
        c2 = Creature(2, 2)
        game = PermanentDamageCardGame([c1, c2])
        winner_index = game.combat(0, 1)
        # no winner: creatures kill one another
        self.assertEqual(winner_index, -1)


if __name__ == "__main__":
    unittest.main(exit=False)
