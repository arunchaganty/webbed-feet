from django.contrib import admin
import models

admin.site.register(models.Game, models.GameAdmin)
admin.site.register(models.Submission, models.SubmissionAdmin)
admin.site.register(models.Run)
