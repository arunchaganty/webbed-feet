from django.db import models

import operator

from web.home import models as home_models
from web.webbing import errors

class Submission( models.Model ):
    team = models.ForeignKey( home_models.Team )
    timestamp = models.DateTimeField( auto_now = True )
    sha1sum = models.CharField( max_length=100 )
    name = models.CharField(max_length=100)
    data = models.FileField( upload_to='bots' )
    comments = models.TextField()

    def get_score(self):
        # Compute score
        player1RunsCount = Run.objects.filter(player1=self).count()
        player2RunsCount = Run.objects.filter(player2=self).count()
        player1Runs = Run.objects.filter(player1=self, score__gt=0)
        player2Runs = Run.objects.filter(player2=self, score__lt=0)

        score = 0
        # When player 1, +ve score is good; when player 2, -ve score is good
        if len(player1Runs) > 0:
            score += reduce(operator.add, [ run.score for run in player1Runs ])
        if len(player2Runs) > 0:
            score += reduce(operator.add, [ -1*run.score for run in player2Runs ])
        count = player1RunsCount + player2RunsCount

        # Compute mean score
        if count > 0:
            score = float(score)/count

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
 
