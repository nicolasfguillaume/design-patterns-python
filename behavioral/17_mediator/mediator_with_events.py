# same Event class as in the Chain of Responsibility pattern
# list of functions we can call whenever something happens
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


# central mediator
class Game:
    def __init__(self):
        self.events = Event()

    # invoke the event and make sure that everybody who subscribes to this event actually 
    # gets the information and we can define what those args actually are.
    def fire(self, args):
        self.events(args)


class GoalScoredInfo:
    def __init__(self, who_scored, goals_scored):
        self.goals_scored = goals_scored
        self.who_scored = who_scored


class Player:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.goals_scored = 0

    def score(self):
        self.goals_scored += 1
        # we generate this GoalScoredInfo structure
        args = GoalScoredInfo(self.name, self.goals_scored)
        # then we send it off to the event o that every subscriber actually gets a copy of this information.
        self.game.fire(args)


class Coach:
    def __init__(self, game):
        # The coach need to subscribe to the game's events in order to celebrate the goal.
        game.events.append(self.celebrate_goal)

    def celebrate_goal(self, args):
        # args can be any object
        if isinstance(args, GoalScoredInfo) and args.goals_scored < 3:
            print(f'Coach says: well done, {args.who_scored}!')


if __name__ == '__main__':
    game = Game()
    player = Player('Sam', game)
    coach = Coach(game)

    player.score()  # Coach says: well done, Sam!
    player.score()  # Coach says: well done, Sam!
    player.score()  # ignored by coach
