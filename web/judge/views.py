# Create your views here.

from django.shortcuts import render_to_response 
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import forms
import models
import web.registration.models as r_models

from django.core import exceptions

from web import settings

from web.home.decorators import login_required

RUNS_PER_PAGE = 25


@login_required()
def manage(request):
    if request.POST:
        data = request.POST
        file_data = request.FILES
        sub = models.Submission(team = request.session["team"])
        form = forms.SubmissionForm(data=data, files=file_data, instance=sub)
        if form.is_valid():
            form.save()
            # Set the first 5 bots 'active', and make all the rest inactive
            bots = models.Submission.objects.filter(team = request.session["team"], active=True).order_by('-timestamp')
            if len(bots) > settings.MAX_ACTIVE_BOTS:
                for bot in bots[settings.MAX_ACTIVE_BOTS:]: 
                    bot.active = False
                    bot.save()
    else:
        form = forms.SubmissionForm()

    submissions = models.Submission.objects.filter(team = request.session["team"]).order_by('-timestamp')

    return render_to_response("manage.html", 
            {'form':form,
            'submissions':submissions},
            context_instance = RequestContext(request))

def standings(request):
    # Get the best bot for every team
    # TODO: Make query more efficient
    scores = {}
    bots = models.Submission.objects.all()
    for team in r_models.Team.objects.all():
        # Get bots' scores
        s = map( lambda t: t.score, bots.filter(team = team))
        if s:
            scores[team] = max(s)
    
    scores = scores.items()
    scores.sort(key=lambda ts: ts[1], reverse=True)
    scores = [ (p,) + s for (p,s) in zip(range(1,len(scores)+1), scores) ]
        
    return render_to_response("standings.html", 
            {'scores':scores},
            context_instance = RequestContext(request))

def results(request, bot_id=None, page=1):
    if bot_id != None:
        try:
            bot = models.Submission.objects.get(id=bot_id)
            runs = bot.player1_runset.all() | bot.player2_runset.all()
            runs = runs.order_by('-timestamp')
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "No bot by that id exists")
            return HttpResponseRedirect("/judge/results/all/")
    else:
        runs = models.Run.objects.order_by('-timestamp')

    # Paginate results
    paginator = Paginator( runs, RUNS_PER_PAGE )
    try:
        displayed_runs = paginator.page(page)
    except:
        displayed_runs = paginator.page(paginator.num_pages)

    return render_to_response("results.html", {
            'bot_id':bot_id,
            'runs':displayed_runs,
            'paginator':paginator,
            },
            context_instance = RequestContext(request))

