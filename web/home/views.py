# Create your views here.

from django.shortcuts import render_to_response 
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import django.contrib.auth as auth 
import django.contrib.auth.views as auth_views 
import forms
import web.registration.models as r_models
import web.events.models as e_models

from web import settings

def home(request):
    if request.POST:
        data = request.POST
        form = forms.LoginForm(data=data)
        if form.is_valid():
            # Check if team exists and is registered for the event
            request.session["team"] = form.instance
            return HttpResponseRedirect("/home/")
    else:
        form = forms.LoginForm(None)
    return render_to_response("home.html", 
            {'form':form,},
            context_instance = RequestContext(request))

def ping(request):
    return HttpResponse("")

def login(request):
    return home(request)

def logout(request):
    if request.session.has_key("team"):
        del request.session["team"]
    return home(request)

