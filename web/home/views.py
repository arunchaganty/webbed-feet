# Create your views here.

from django.shortcuts import render_to_response 
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import forms
import web.registration.models as r_models
import web.events.models as e_models
import web.judge.models as j_models

from django.db.models import Max

from decorators import login_required

from web import settings

def home(request):
    if request.POST:
        data = request.POST
        form = forms.LoginForm(data=data)
        if form.is_valid():
            # Check if team exists and is registered for the event
            request.session["team"] = form.instance
            if request.GET.has_key("next"):
                return HttpResponseRedirect(request.GET["next"])
            else:
                return HttpResponseRedirect("/home/")
    elif request.session.has_key("team"):
        team = request.session["team"]
        bots = j_models.Submission.objects.filter(team=team)
        botCount = bots.count()

        event = e_models.TeamEvent.objects.get(name=settings.EVENT_NAME)
        teams = event.teams.all()
        teams = teams.annotate(score = Max('submission__score'))
        standings = list(teams)
        standings.sort(lambda t: t.score, reverse=True)
        standing = standings.index(team)
        score = standings[standing].score

        return render_to_response("home.html", {
            'botCount':botCount,
            'standing':standing + 1,
            'score':score,
            },
            context_instance = RequestContext(request))
    else: 
        form = forms.LoginForm(None)
        
    return render_to_response("home.html", 
            {'form':form,},
            context_instance = RequestContext(request))

def ping(request):
    return HttpResponse("")

def login(request):
    return home(request)

@login_required()
def logout(request):
    if request.session.has_key("team"):
        del request.session["team"]
    return HttpResponseRedirect("/home/")

