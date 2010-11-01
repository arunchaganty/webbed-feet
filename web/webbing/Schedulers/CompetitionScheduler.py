import Scheduler

RUN_COUNT = 5

class CompetitionScheduler(Scheduler.Scheduler):
    """Schedules games so that all bots get a nearly equal share of matches"""

    @classmethod
    def schedule(cls, game):
        # Only two players
        candidates = game.submission_set.all().order_by("count")

        if len(candidates) < 2:
            print "Insufficient candidates"
            return Scheduler.Task()

        for i in range(RUN_COUNT):
            for player1 in candidates:
                for player2 in candidates:
                    if player1 == player2: continue

                    players = [player1, player2]

                    yield Scheduler.GameRunTask(game.cls, *players)

