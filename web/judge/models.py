from django.db import models

import operator

from web.registration import models as r_models
from web.webbing import errors

class Game( models.Model ):
    name = models.CharField( max_length=100 )
    classname = models.CharField( max_length=100 )
    active = models.BooleanField(default=True)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.name

class Submission( models.Model ):
    game = models.ForeignKey( Game )
    team = models.ForeignKey( r_models.Team )

    timestamp = models.DateTimeField( auto_now = True )
    sha1sum = models.CharField( max_length=100 )

    name = models.CharField(max_length=100)
    data = models.FileField( upload_to='bots' )
    comments = models.TextField(null=True, blank=True)

    active = models.BooleanField()

    count = models.IntegerField(default=0)
    score = models.FloatField(default=0)

    def update_score(self, score):
        self.score = (score  + self.count * self.score) / (self.count + 1)
        self.count += 1

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
 
