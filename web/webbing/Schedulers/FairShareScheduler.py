import Scheduler
import random
import numpy as np

class FairShareScheduler(Scheduler.Scheduler):
    """Schedules games so that all bots get a nearly equal share of
    matches, but does so stochastically so as not to play the _same_
    both over and over again"""


    def choose( dist ):
        dist = normalise( dist )
        idx = np.random.multinomial( 1, dist ).argmax()
        return idx

    def choose_min_randomly( candidates ):
            # Create a multinomial distribution; each is proportional to (1+r).
            preferences = np.array( [ float(candidate.count) for candidate in candidates ] )
            preferences = 1/(1.0 + preferences)

            return candidates[ choose( preferences ) ]


    @classmethod
    def schedule(cls, game):
        while True:
            # Only two players
            candidates = game.submission_set.filter(active=True, user__is_active = True)
            
            # If no candidates, just return a 'waste-time' task
            if len(candidates) < 2:
                print "Insufficient candidates"
                yield Scheduler.Task()
                continue


            player1 = choose_min_randomly( candidates )
            candidates_ = [c for c in candidates[1:] if c.user != player1.user]
            players = [player1, choose_min_randomly( candidates_ ) ]

            # Choose a start position at random
            random.shuffle(players)
            
            print "%s chosen from %d candidates"%( players, len( candidates ) )

            yield Scheduler.GameRunTask(game.cls, *players)

