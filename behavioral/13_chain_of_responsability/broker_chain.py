# 1) event broker (that takes care of the chain of responsibility)
# 2) command-query separation (cqs)
# 3) observer
from abc import ABC
from enum import Enum


# an event is a list of callables (functions that we can call)
# that can be called in sequence with the same arguments
class Event(list):
    def __call__(self, *args, **kwargs):
        # iterates over each item in the list
        for item in self:
            # each item in the list is called as a function with the provided arguments
            item(*args, **kwargs)


class WhatToQuery(Enum):
    ATTACK = 1
    DEFENSE = 2


class Query:
    def __init__(self, creature_name, what_to_query, default_value):
        # value that subsequently other handlers of the event can modify
        self.value = default_value  # bidirectional (creature modifiers can change the value)
        self.what_to_query = what_to_query
        self.creature_name = creature_name


# (centralized) event broker
class Game:
    def __init__(self):
        # this event is something that anybody can subscribe to, whenever somebody sends a query
        self.queries = Event()

    # somebody sends a query for a creature attack, but the modifier can listen to this event, and they can modify the returning value
    def perform_query(self, sender, query):
        # we call on the event with the sender and the query
        # each callable functions in the Event list is called with the same arguments sender and query
        self.queries(sender, query)


class Creature:
    def __init__(self, game, name, attack, defense):
        self.initial_defense = defense  # inital values, not final
        self.initial_attack = attack
        self.name = name
        self.game = game  # event broker

    @property
    def attack(self):
        # performs a query using the event broker, to return the attack value
        q = Query(self.name, WhatToQuery.ATTACK, self.initial_attack)
        self.game.perform_query(self, q)
        return q.value

    @property
    def defense(self):
        # performs a query using the event broker, to return the defense value
        q = Query(self.name, WhatToQuery.DEFENSE, self.initial_attack)
        self.game.perform_query(self, q)
        return q.value

    def __str__(self):
        return f'{self.name} ({self.attack}/{self.defense})'


class CreatureModifier(ABC):
    def __init__(self, game, creature):
        self.creature = creature
        self.game = game
        # changes the query so that the return value is modified
        self.game.queries.append(self.handle)

    def handle(self, sender, query):
        pass

    # happens when entering the with block
    def __enter__(self):
        return self

    # happens when leaving the with block
    def __exit__(self, exc_type, exc_val, exc_tb):
        # here we unsuscribe ourselves from the handlers
        # this remove ourselves from the set of listeners to the queries event, and hence we no longer apply the modifier
        self.game.queries.remove(self.handle)


class DoubleAttackModifier(CreatureModifier):
    # check if, in this particular query, the sender is the name of the creature we have ourselves applied to
    # and somebody is querying the attack value
    def handle(self, sender, query):
        if (sender.name == self.creature.name and
                query.what_to_query == WhatToQuery.ATTACK):
            query.value *= 2


class IncreaseDefenseModifier(CreatureModifier):
    def handle(self, sender, query):
        if (sender.name == self.creature.name and
                query.what_to_query == WhatToQuery.DEFENSE):
            query.value += 3


if __name__ == '__main__':
    game = Game()
    goblin = Creature(game, 'Strong Goblin', 2, 2)
    print(goblin)

    with DoubleAttackModifier(game, goblin):
        # when we enter the scope, the modifier is applied
        print(goblin)
        with IncreaseDefenseModifier(game, goblin):
            print(goblin)

    # when we leave the scope, the modifier is removed (we unsubscribe from the query)
    # so we no longer modify the query, and hence this modifier does not apply
    print(goblin)
