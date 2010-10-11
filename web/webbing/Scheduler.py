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
    #    candidates = self.game.listBots()
#
 #       for player1 in _candidates:
  #          for player2 in _candidates:
   #             yield Task.GameRunTask(self.game.getClass(), player1, player2)
# Only two players
	cand = self.game.listBots()
	for i in range(1):  #len(cand) earlier
            candidates = self.game.listBots()
            print "# of candidates: %d"%(len(candidates))
            # If no candidates, just return a 'waste-time' task
            if len(candidates) == 0:
                yield Task.Task()

            player1 = self.game.listBots(order_by = "count", limit=2)[1]
            candidates = [ c for c in candidates if c.team_id != player1.team_id ]
            if len(candidates) == 0: 
                yield Task.Task()
            else:
		for i in range(26,len(candidates)):
                    players = [player1, candidates[i]]
		    #print players[0].team_id, players[1].team_id
		    #cnt=0
		    #while 1 : cnt=cnt+1
                    yield Task.GameRunTask(self.game.getClass(), *players)
		    
class CompetitionScheduler2(Scheduler):
    """Schedules games so that all bots play all other bots exactly once"""

    def __iter__(self):
	cand = self.game.listBots()

	start1=0 #bot1
	start2=0 #bot2

	for i in range(start1,len(cand)):  
            print "# of candidates: %d"%(len(cand))

            # If no candidates, just return a 'waste-time' task
            #if len(candidates) == 0:
            #    yield Task.Task()

	    player1 = cand[i]

	    if start2 !=-1:
	  	s2 = start2
	    else: 
		s2=0
	    for j in range(s2,len(cand)):
		if cand[j].team_id!=player1.team_id: 
                    players = [player1, cand[j]]
		    #print players[0].team_id, players[1].team_id
		    #cnt=0
		    #while 1 : cnt=cnt+1
                    yield Task.GameRunTask(self.game.getClass(), *players)
      	    start2=-1
		    
