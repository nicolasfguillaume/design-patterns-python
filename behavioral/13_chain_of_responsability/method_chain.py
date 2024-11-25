class Creature:
    def __init__(self, name, attack, defense):
        self.defense = defense
        self.attack = attack
        self.name = name

    def __str__(self):
        return f'{self.name} ({self.attack}/{self.defense})'


class CreatureModifier:
    def __init__(self, creature):
        self.creature = creature
        # defines the next modifier in the chain (there can be multiple modifiers on a creature)
        # every modifier applies one after another
        self.next_modifier = None

    # add a new modifier to the chain
    def add_modifier(self, modifier):
        # if we already have a next_modifier
        if self.next_modifier:
            # then we call a modifier on the next modifier
            self.next_modifier.add_modifier(modifier)
        else:
            # otherwise, we store it
            self.next_modifier = modifier

    # this is the location where this modifier gets applied to the creature
    # this method does not do anything by itself, it is up to the inheriters to add functionality
    # the base class handle is the one that propagates the chain of responsibility
    def handle(self):
        if self.next_modifier:
            self.next_modifier.handle()


class NoBonusesModifier(CreatureModifier):
    def handle(self):
        # here we are not calling the base class handle method
        # hence we are not applying the chain of responsibility (and hence not applying the other modifiers)
        print('No bonuses for you!')


class DoubleAttackModifier(CreatureModifier):
    def handle(self):
        print(f'Doubling {self.creature.name}''s attack')
        self.creature.attack *= 2
        # call the handle method of the base class
        super().handle()


class IncreaseDefenseModifier(CreatureModifier):
    def handle(self):
        if self.creature.attack <= 2:
            print(f'Increasing {self.creature.name}''s defense')
            self.creature.defense += 1
        super().handle()


if __name__ == '__main__':
    goblin = Creature('Goblin', 1, 1)
    print(goblin)

    # top level element (does not do anything)
    root = CreatureModifier(goblin)

    root.add_modifier(NoBonusesModifier(goblin))

    root.add_modifier(DoubleAttackModifier(goblin))
    root.add_modifier(DoubleAttackModifier(goblin))

    # no effect
    root.add_modifier(IncreaseDefenseModifier(goblin))

    root.handle()  # apply modifiers
    print(goblin)
