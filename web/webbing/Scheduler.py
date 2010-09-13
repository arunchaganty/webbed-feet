# Various competition scheduling algorithms
#

import random
import Task
import Game

class Scheduler:
    def __init__(self, game):
        self.game = game
        pass

class MinRunScheduler(Scheduler):
    """Schedules games so that all bots get a nearly equal share of matches"""

    def __iter__(self):
        while True:
            # Only two players
            candidates = self.game.listBots()
            print "# of candidates: %d"%(len(candidates))
            # If no candidates, just return a 'waste-time' task
            if len(candidates) == 0:
                yield Task.Task()

            player1 = self.game.listBots(order_by = "count", limit=1)[0]
            candidates = [ c for c in candidates if c.team_id != player1.team_id ]
            if len(candidates) == 0: 
                yield Task.Task()
            else:
                players = [player1, random.choice(candidates)]

            # Choose a start position at random
            random.shuffle(players)

            yield Task.GameRunTask(self.game.getClass(), *players)

class CompetitionScheduler(Scheduler):
    """Schedules games so that all bots play all other bots exactly once"""

    def __iter__(self):
        candidates = self.game.listBots()

        for player1 in _candidates:
            for player2 in _candidates:
                yield Task.GameRunTask(self.game.getClass(), player1, player2)

