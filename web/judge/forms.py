from django import forms
from django.db import models as d_models

from scheduler import gbl

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
        self.process_binary()
        self.cleaned_data["data"].name = self.cleaned_data["sha1sum"]
        print self.cleaned_data["data"].size
        self.instance.sha1sum = self.cleaned_data["sha1sum"]
        return self.cleaned_data

    # TODO: Check binary for validity, etc.

    def clean_sha1sum(self):
        data = self.cleaned_data["data"]
        self.cleaned_data["sha1sum"] = hashlib.sha1(data.read()).hexdigest()

    def process_binary(self):
        if gbl.POST_SUBMISSION_HOOK != None:
            data = self.cleaned_data["data"]
            data = gbl.POST_SUBMISSION_HOOK(data)
            self.cleaned_data["data"].truncate(0)
            self.cleaned_data["data"].write(data)
            self.cleaned_data["data"].close()


