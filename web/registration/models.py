from django.db import models

from django.contrib.auth.models import User 
# Django's Admin interface - it's awesome.
from django.contrib import admin

# Create your models here.
class Team( models.Model ):
    name = models.CharField( max_length = 255 )
    password = models.CharField( max_length = 255 )
    leader = models.IntegerField()

    def __str__(self):
        return self.name

    class Admin:
        pass


