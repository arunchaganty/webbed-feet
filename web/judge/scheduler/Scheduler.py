# Various competition scheduling algorithms
#

import random
import Task

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
            players = [self.pool.min(), random.choice(candidates)]
            # Choose a start position at random
            random.shuffle(players)
            print players[0]
            print players[1]

            yield Task.DBTestTask(self.pool, *players)

class CompetitionScheduler(Scheduler):
    """Schedules games so that all bots play all other bots exactly once"""

    def __iter__(self):
        _candidates = self.candidates

        for player1 in _candidates:
            for player2 in _candidates:
                yield Task.Task(player1, player2)

