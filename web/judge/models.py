from django.db import models

import operator

from web.home import models as home_models
from web.webbing import errors

class Submission( models.Model ):
    team = models.ForeignKey( home_models.Team )
    timestamp = models.DateTimeField( auto_now = True )
    sha1sum = models.CharField( max_length=100 )
    data = models.FileField( upload_to='bots' )
    comments = models.TextField()

    def get_score(self):
        # Compute score
        player1Runs = Run.objects.filter(player1=self)
        player2Runs = Run.objects.filter(player2=self)

        score = 0
        # When player 1, +ve score is good; when player 2, -ve score is good
        if player1Runs:
            score += reduce(operator.add, [ run.score for run in player1Runs if run.score > 0 ])
        if player2Runs:
            score += reduce(operator.add, [ run.score for run in player2Runs if run.score < 0 ])

        return score
    score = property(get_score)

    def get_runCount(self):
        # Compute score
        player1Runs = Run.objects.filter(player1=self).count()
        player2Runs = Run.objects.filter(player2=self).count()

        return player1Runs + player2Runs
    runCount = property(get_runCount)

    def __unicode__(self):
        return "[Submission %s]"%(self.sha1sum)

    class Admin:
        pass

class Run( models.Model ):
    STATUS = errors.STATUS

    timestamp = models.DateTimeField( auto_now = True )
    player1 = models.ForeignKey( Submission, related_name="player1_runset" )
    player2 = models.ForeignKey( Submission, related_name="player2_runset" )
    score = models.IntegerField()
    status = models.CharField(max_length=3, choices=STATUS)
    game_data = models.FileField(upload_to='logs')

    class Admin:
        pass
 
