from django import forms
from django.db import models as d_models

from web.webbing import errors
from web.webbing.Games import Game

import settings
import models

import hashlib

class SubmissionForm( forms.ModelForm ):
    """Used to submit a bot"""

    data = forms.FileField(label="Bot Code")
    class Meta:
        model = models.Submission
        fields = ('game', 'name', 'data', 'comments')

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

    def clean_name(self):
        name = self.cleaned_data["name"]

        if len(models.Submission.objects.filter(user=self.instance.user, name=name)) > 0:
            raise forms.ValidationError("You already have a bot by this name")
        
        return name

    def clean_sha1sum(self):
        data = self.cleaned_data["data"]
        data.open('rb')
        hsh = hashlib.sha1()
        while True:
            bits = data.read(128)
            if not bits:
                break
            hsh.update(bits)
        self.cleaned_data["sha1sum"] = hsh.hexdigest()
        data.close()

    def clean_data(self):
        game = self.cleaned_data["game"]

        # Get the game class
        try:
            cls = game.cls
        except AttributeError:
            raise forms.ValidationError("Error in judge. Please contact event coordinators")

        data = self.cleaned_data["data"]

        try:
            data = cls.submissionHook(data)
        except errors.GameError, e:
            raise forms.ValidationError(str(e))

        return data


