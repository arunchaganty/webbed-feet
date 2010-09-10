from django import forms
from django.db import models as d_models
from django.contrib.auth import forms as auth_forms

import models

class LoginForm( auth_forms.AuthenticationForm ):
    pass

# TODO: Forms to modify teams

