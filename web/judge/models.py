from django.db import models
from django.db import transaction
from django.contrib import admin

import operator

from web.home.models import User
from web.webbing import errors
from web.webbing import Games
from web.webbing import Schedulers

class Game( models.Model ):
    """Defines a type of game. 
    @classname corresponds to a class in the module web.webbing.Game """
    name = models.CharField( max_length=100 )
    classname = models.CharField( max_length=100 )
    schedulername = models.CharField( max_length=100 )
    active = models.BooleanField( default=True )
    weight = models.FloatField(default=1.0)
    dirty = models.BooleanField( default=False ) # Whether webbing should reset itself or not

    def get_class(self):
        # Try to import a class from Games
        mod = __import__("web.webbing.Games.%s"%(self.classname), fromlist=[Games])
        assert( hasattr(mod, self.classname) )
        cls = getattr( mod, self.classname )

        return cls
    cls = property(get_class)

    def get_scheduler(self):
        # Try to import a class from Games
        mod = __import__("web.webbing.Schedulers.%s"%(self.schedulername), fromlist=[Schedulers])
        assert( hasattr(mod, self.schedulername) )
        scheduler = getattr( mod, self.schedulername )

        return scheduler
    scheduler = property(get_scheduler)

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
    src = models.FileField( upload_to='bot_src' )
    data = models.FileField( upload_to='bots' )
    comments = models.TextField(null=True, blank=True)

    active = models.BooleanField()

    # Fail Count to prevent failed bots from running continuously
    failures = models.IntegerField(default=0)

    # Score stored here for efficent reads
    count = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    
    def update_score(self, score):
        self.score = (score  + self.count * self.score) / (self.count + 1)
        self.count += 1

    def __unicode__(self):
        return "[Submission %s]"%(self.sha1sum)

class SubmissionAdmin( admin.ModelAdmin ):
    list_display = ('name', 'user', 'game')
    search_fields = ['user__username']


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

    @classmethod
    @transaction.commit_on_success()
    def add_run(cls, run_data):
        timestamp, player1, player2, score1, score2, status, game_data = run_data
            
        run = cls.objects.create(
                player1 = player1,
                player2 = player2,
                score1 = score1,
                score2 = score2,
                status = status,
                game_data = game_data
                )

        # Player 1
        count = player1.count + 1
        if status in ["OK"]:
            player1.score = (score1 + player1.score * player1.count) / float(count)
            player1.failures = 0
        elif status in ["DQ2", "TO2", "CR2"]:  
            player1.score = (score1 + player1.score * player1.count) / float(count)
        elif status in ["DQ1", "TO1", "CR1"]:  
            player1.failures += 1 
            if player1.failures == gbl.FAIL_CHANCES:
                player1.active = False
        player1.count += 1
        player1.save()

        # Player2
        player2 = player2
        count = player2.count + 2
        if status in ["OK"]:
            player2.score = (score2 + player2.score * player2.count) / float(count)
            player2.failures = 0
        elif status in ["DQ2", "TO2", "CR2"]:  
            player2.score = (score2 + player2.score * player2.count) / float(count)
        elif status in ["DQ2", "TO2", "CR2"]:  
            player2.failures += 2 
            if player2.failures == gbl.FAIL_CHANCES:
                player2.active = False
        player2.count += 2
        player2.save()

@transaction.commit_on_success()
def reset_game(modeladmin, request, queryset):
    for game in queryset:
        Run.objects.filter(player1__game=game).delete()
        Submission.objects.filter(game=game).update(score=0, failures=0, count=0)

        # Set the dirty bit
        game.dirty = True
        game.save()
reset_game.short_description = "Reset Game"

class GameAdmin( admin.ModelAdmin ):
    actions = [reset_game]

