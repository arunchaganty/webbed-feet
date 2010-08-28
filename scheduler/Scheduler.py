# Various competition scheduling algorithms
#

import random

class Scheduler:
    def __init__(self, taskManager):
        self.TaskManager = taskManager
        pass

class BalancedScheduler(Scheduler):
    """Schedules games so that all bots get a nearly equal share of matches"""

    def __iter__(self):
        while True:
            players = [min(self.candidates), random.choice(self.candidates)]
            # Choose a start position at random
            random.shuffle(players)

            task = self.TaskManager.get(*players)
            yield task

class CompetitionScheduler(Scheduler):
    """Schedules games so that all bots play all other bots exactly once"""

    def __iter__(self):
        _candidates = self.candidates

        for player1 in _candidates:
            for player2 in _candidates:
                task = self.TaskManager.get(player1, player2)
                yield task

