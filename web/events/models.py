from django.db import models
from web.registration import models as r_models

# Create your models here.
class TeamEvent( models.Model ):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,blank=True,verify_exists=False)
    registerable = models.BooleanField()
    hospi_only=models.BooleanField(default=False)
    logo=models.FileField(upload_to="logos/", blank=True, null=True)
    size = models.SmallIntegerField()
    min_size = models.SmallIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    teams = models.ManyToManyField(r_models.Team, blank=True, null=True, related_name='events')
    
    def __str__(self):
        return self.name

    class Admin:
        pass

