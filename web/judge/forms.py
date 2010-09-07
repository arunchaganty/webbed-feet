from django import forms
from django.db import models as d_models

import settings
import models

import hashlib

class SubmissionForm( forms.ModelForm ):
    data = forms.FileField(label="Bot Binary")
    class Meta:
        model = models.Submission
        exclude = ('timestamp','team', 'sha1sum')

    def clean(self):
        forms.ModelForm.clean(self)
        self.clean_sha1sum()
        self.clean_binary()
        self.cleaned_data["data"].name = self.cleaned_data["sha1sum"]
        print self.cleaned_data["data"].size
        self.instance.sha1sum = self.cleaned_data["sha1sum"]
        return self.cleaned_data

    # TODO: Check binary for validity, etc.

    def clean_sha1sum(self):
        data = self.cleaned_data["data"]
        self.cleaned_data["sha1sum"] = hashlib.sha1(data.read()).hexdigest()

    def clean_binary(self):
        if settings.POST_SUBMISSION_HOOK != None:
            data = self.cleaned_data["data"]
            settings.POST_SUBMISSION_HOOK(data)

