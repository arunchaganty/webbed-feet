from django import forms
from django.db import models as d_models

from django.core import exceptions

import web.settings as settings
import web.registration.models as r_models
import web.events.models as e_models

import hashlib

class LoginForm( forms.ModelForm ):
    name = forms.CharField(label="Team Name")
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = r_models.Team
        exclude = ('leader')

    def clean(self):
        forms.ModelForm.clean(self)

        if self.is_valid():
            # Check if the team exists
            try:
                team = r_models.Team.objects.get(name=self.cleaned_data["name"], password=self.cleaned_data["password"])
                event = e_models.TeamEvent.objects.get(name=settings.EVENT_NAME)

                if len(event.teams.filter(id=team.id)) > 0:
                    self.instance = team
                else:
                    raise exceptions.ValidationError("Team not registered for event.\n Please register on the Userportal")

            except exceptions.ObjectDoesNotExist:
                raise exceptions.ValidationError("Team does not exist, or incorrect password.\n Please register on the Userportal")

        return self.cleaned_data


    def clean_password(self):
        passwd = self.cleaned_data["password"]
        passwd = hashlib.md5(passwd).hexdigest()

        return passwd

# TODO: Forms to modify teams

