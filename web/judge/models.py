from django.db import models

import operator

from web.home.models import User
from web.webbing import errors
from web.webbing import Games

class Game( models.Model ):
    """Defines a type of game. 
    @classname corresponds to a class in the module web.webbing.Game """
    name = models.CharField( max_length=100 )
    classname = models.CharField( max_length=100 )
    active = models.BooleanField( default=True )
    weight = models.FloatField(default=1.0)

    def get_class(self):
        # Try to import a class from Games
        mod = __import__("web.webbing.Games.%s"%(self.classname), fromlist=[Games])
        assert( hasattr(mod, self.classname) )
        cls = getattr( mod, self.classname )

        return cls
    cls = property(get_class)

    def __str__(self):
        return self.name

class Submission( models.Model ):
    """ A submitted entity """

    game = models.ForeignKey( Game )
    user = models.ForeignKey( User )

    # Consistency metadata
    timestamp = models.DateTimeField( auto_now = True )
    sha1sum = models.CharField( max_length=100 )

    # Actual contents
    name = models.CharField(max_length=100)
    data = models.FileField( upload_to='bots' )
    comments = models.TextField(null=True, blank=True)

    active = models.BooleanField()

    # Score stored here for efficent reads
    count = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    
    def update_score(self, score):
        self.score = (score  + self.count * self.score) / (self.count + 1)
        self.count += 1

    def __unicode__(self):
        return "[Submission %s]"%(self.sha1sum)

class Run( models.Model ):
    """Actual run of the game"""
    STATUS = errors.STATUS

    timestamp = models.DateTimeField( auto_now = True )
    player1 = models.ForeignKey( Submission, related_name="player1_runset" )
    player2 = models.ForeignKey( Submission, related_name="player2_runset" )
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    status = models.CharField(max_length=3, choices=STATUS)
    game_data = models.FileField(upload_to='logs')
 
