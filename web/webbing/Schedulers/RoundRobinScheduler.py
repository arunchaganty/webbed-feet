import Scheduler

class RoundRobinScheduler(Scheduler.Scheduler):
    """Schedules games in a round robin, playing every bot with every other"""

    @classmethod
    def schedule(cls, game):
        while True:
            # Only two players
            candidates = game.submission_set.filter(active=True, user__is_active = True).order_by("count")

            if len(candidates) < 2:
                print "Insufficient candidates"
                yield Scheduler.Task()

            # Choose min candidate
            player1 = candidates[0]

            # And play against everyone else
            for player2 in candidates:
                if player1.user == player2.user: continue

                players = [player1, player2]
                yield Scheduler.GameRunTask(game.cls, *players)

                players = [player2, player1]
                yield Scheduler.GameRunTask(game.cls, *players)

