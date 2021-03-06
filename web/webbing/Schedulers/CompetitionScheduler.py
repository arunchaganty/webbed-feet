import Scheduler

RUN_COUNT = 2

class CompetitionScheduler(Scheduler.Scheduler):
    """Schedules games so that all bots get a nearly equal share of matches"""

    @classmethod
    def schedule(cls, game):
        # Only two players
        candidates = game.submission_set.filter(active=True, user__is_active = True).order_by("count")

        if len(candidates) < 2:
            print "Insufficient candidates"
            yield Scheduler.Task()

        for i in range(RUN_COUNT):
            for player1 in candidates:
                for player2 in candidates:
                    if player1.user == player2.user: continue

                    players = [player1, player2]

                    yield Scheduler.GameRunTask(game.cls, *players)

