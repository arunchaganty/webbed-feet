from django import forms
from django.db import models as d_models

import game
from web.webbing import errors

import settings
import models

import hashlib

class SubmissionForm( forms.ModelForm ):
    data = forms.FileField(label="Bot Binary")
    class Meta:
        model = models.Submission
        exclude = ('timestamp', 'team', 'sha1sum', 'active')

    def clean(self):
        forms.ModelForm.clean(self)

        if self.is_valid():
            # Add the SHA1SUM
            self.clean_sha1sum()

            # Rename the file by it's SHA1SUM
            self.cleaned_data["data"].name = self.cleaned_data["sha1sum"]
            self.instance.sha1sum = self.cleaned_data["sha1sum"]
            self.instance.active = True

        return self.cleaned_data

    def clean_sha1sum(self):
        data = self.cleaned_data["data"]
        self.cleaned_data["sha1sum"] = hashlib.sha1(data.read()).hexdigest()

    def clean_data(self):
        data = self.cleaned_data["data"]
        if game.BOT_SUBMISSION_HOOK != None:
            # Pass the data through the hook
            try:
                data = game.BOT_SUBMISSION_HOOK(data)
            except errors.GameError as e:
                raise forms.ValidationError(str(e))
        return data


