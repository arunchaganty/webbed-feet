from django.db import models

# Django's Admin interface - it's awesome.
from django.contrib import admin

# Just define the 'User'
from django.contrib.auth.models import User

class Notice( models.Model ):
    SUMMARY_LEN = 20
    timestamp = models.DateTimeField( )
    message = models.TextField( null=True, blank=True )

    def __str__(self):
        return self.message

    def __repr__(self):
        if len(self.message) > SUMMARY_LEN:
            return self.message[0:SUMMARY_LEN] + "..."
        else:
            return self.message

