# Various competition scheduling algorithms
#

import random
import Task
import Game

class Scheduler:
    def __init__(self, pool):
        self.pool = pool
        pass

class MinRunScheduler(Scheduler):
    """Schedules games so that all bots get a nearly equal share of matches"""

    def __iter__(self):
        while True:
            # Only two players
            candidates = self.pool.all()
            print "# of candidates: %d"%(len(candidates))

            minPlayer = self.pool.min()
            if minPlayer != None:
                players = [minPlayer, random.choice(candidates)]
            else:
                players = [random.choice(candidates), random.choice(candidates)]
            # Choose a start position at random
            random.shuffle(players)
            print players

            yield Task.GameRunTask(Game.SnakeGame, *players)

class CompetitionScheduler(Scheduler):
    """Schedules games so that all bots play all other bots exactly once"""

    def __iter__(self):
        _candidates = self.pool.all()

        for player1 in _candidates:
            for player2 in _candidates:
                yield Task.GameRunTask(player1, player2)

