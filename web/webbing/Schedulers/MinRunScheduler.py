import Scheduler
import random

class MinRunScheduler(Scheduler.Scheduler):
    """Schedules games so that all bots get a nearly equal share of matches"""

    @classmethod
    def schedule(cls, game):
        while True:
            # Only two players
            candidates = game.submission_set.filter(active=True, user__is_active = True).order_by("count")
            
            # If no candidates, just return a 'waste-time' task
            if len(candidates) < 2:
                print "Insufficient candidates"
                yield Scheduler.Task()
                continue

            player1 = candidates[0]
            candidates_ = [c for c in candidates[1:] if c.user != player1.user]
            players = [player1, random.choice(candidates_)]

            # Choose a start position at random
            random.shuffle(players)
            
            print "%s chosen from %d candidates"%( players, len( candidates ) )

            yield Scheduler.GameRunTask(game.cls, *players)

