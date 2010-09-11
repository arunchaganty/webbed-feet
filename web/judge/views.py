# Create your views here.

from django.shortcuts import render_to_response 
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import forms
import models
import web.registration.models as r_models
import web.events.models as e_models
from django.db.models import Max

from django.core import exceptions

from web import settings

from web.home.decorators import login_required

RUNS_PER_PAGE = 25
TEAMS_PER_PAGE = 25


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

def standings(request, page=1, gameName=None):
    games = models.Game.objects.all()


    if gameName:
        try: 
            game = games.get(name=gameName)
            # Get the best bot for every team
            submissions = models.Submission.objects.filter(game = game)
            teams = submissions.values("team__name").annotate(score=Max('score')).order_by('-score')

            standings = list(teams)
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "No game by that name exists")
            return HttpResponseRedirect("/judge/standings/all/")
    else:
        team_score = {}
        for game in games:
            # Get the best bot for every team
            submissions = models.Submission.objects.filter(game=game)
            teams = submissions.values("team__name").annotate(score=Max('score'))
            for team in teams:
                if not team_score.has_key(team["team__name"]):
                    team_score[team["team__name"]] = 0
                team_score[team["team__name"]] += team["score"] * game.weight

        teams = team_score.items()
        teams.sort(key=lambda kv: kv[1], reverse=True)
        standings = [{'team__name':kv[0], 'score':kv[1]} for kv in teams]

    paginator = Paginator( standings, TEAMS_PER_PAGE )
    try:
        displayed_teams = paginator.page(page)
    except:
        displayed_teams = paginator.page(paginator.num_pages)

    return render_to_response("standings.html", {
        'standings':displayed_teams,
        'games':games,
        
        },
            context_instance = RequestContext(request))

def results(request, bot_id=None, page=1, gameName=None):
    # Game
    bot = None
    game = None
    games = models.Game.objects.all()

    if gameName != None:
        try:
            game = models.Game.objects.get(name=gameName)
            runs = models.Run.objects.filter(player1__game=game)
            runs = runs.order_by('-timestamp')
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "No game by that name exists")
            return HttpResponseRedirect("/judge/results/all/")
    elif bot_id != None:
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
            'bot': bot,
            'game': game,
            'games': games,
            'runs':displayed_runs,
            'paginator':paginator,
            },
            context_instance = RequestContext(request))

