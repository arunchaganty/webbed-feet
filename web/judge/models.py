from django.db import models

from web.home import models as home_models

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
        score += [ run.score for run in player1Runs if run.score > 0 ]
        score += [ run.score for run in player2Runs if run.score < 0 ]

        return score
    score = property(get_score)

    def __unicode__(self):
        return "[Submission %s]"%(self.sha1sum)

    class Admin:
        pass

class Run( models.Model ):
    STATUS = (
        ('OK', 'No Errors'),
        ('DQ1', 'Player 1 Disqualified'),
        ('DQ2', 'Player 2 Disqualified'),
        ('TO1', 'Player 1 Timed Out'),
        ('TO2', 'Player 2 Timed Out'),
        ('CR1', 'Player 1 Crashed'),
        ('CR2', 'Player 2 Crashed'),
        ('ERR', 'Unknown Error'),
        )

    timestamp = models.DateTimeField( auto_now = True )
    player1 = models.ForeignKey( Submission, related_name="player1_runset" )
    player2 = models.ForeignKey( Submission, related_name="player2_runset" )
    score = models.IntegerField()
    status = models.CharField(max_length=3, choices=STATUS)
    game_data = models.FileField(upload_to='runs')

    class Admin:
        pass
 
