# Create your views here.

from django.shortcuts import render_to_response 
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import forms
import models
from django.db.models import Max

from django.core import exceptions

from django.contrib.auth.decorators import login_required
from web import settings

RUNS_PER_PAGE = 25
USERS_PER_PAGE = 50

@login_required()
def manage(request):
    """ Handles uploading of bots """

    if request.POST:
        data = request.POST
        file_data = request.FILES
        sub = models.Submission(user = request.user)
        form = forms.SubmissionForm(data=data, files=file_data, instance=sub)
        if form.is_valid():
            form.save()
            # Set the first MAX_ACTIVE_BOTS bots 'active', and make all the rest inactive
            bots = models.Submission.objects.filter(user = request.user, active=True).order_by('-timestamp')
            if len(bots) > settings.MAX_ACTIVE_BOTS:
                for bot in bots[settings.MAX_ACTIVE_BOTS:]: 
                    bot.active = False
                    bot.save()
    else:
        form = forms.SubmissionForm()

    submissions = models.Submission.objects.filter(user = request.user).order_by('-timestamp')

    return render_to_response("manage.html", 
            {'form':form,
            'submissions':submissions},
            context_instance = RequestContext(request))

def standings(request, page=1, gameName=None):
    """Create a standings listing"""
    games = models.Game.objects.filter(active=True)

    if gameName:
        try: 
            game = games.get(name=gameName)
            # Get the best bot for every user
            submissions = models.Submission.objects.filter(game = game)
            users = submissions.filter(active=True).values("user__username").annotate(score=Max('score')).order_by('-score').values("name", "user__username", "score")

            standings = list(users)
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "No game by that name exists")
            return HttpResponseRedirect("%s/judge/standings/all/"%(settings.SITE_URL,))
    else:
        user_score = {}
        for game in games:
            # Get the best bot for every user
            submissions = models.Submission.objects.filter(game=game)
            users = submissions.filter(active=True).values("user_username").annotate(score=Max('score'))
            for user in users:
                if not user_score.has_key(user["user__username"]):
                    user_score[user["user__username"]] = 0
                user_score[user["user_username"]] += user["score"] * game.weight

        users = user_score.items()
        users.sort(key=lambda kv: kv[1], reverse=True)
        standings = [{'username':kv[0], 'score':kv[1]} for kv in users]

    paginator = Paginator( standings, USERS_PER_PAGE )
    try:
        displayed_users = paginator.page(page)
    except:
        displayed_users = paginator.page(paginator.num_pages)

    return render_to_response("standings.html", {
        'gameName':gameName,
        'standings':displayed_users,
        'games':games,
        
        },
            context_instance = RequestContext(request))

def results(request, bot_id=None, page=1, gameName=None):
    # Game
    bot = None
    game = None
    games = models.Game.objects.filter(active=True)

    if gameName != None:
        try:
            game = games.get(name=gameName)
            runs = models.Run.objects.filter(player1__game=game)
            runs = runs.order_by('-timestamp')
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "No game by that name exists")
            return HttpResponseRedirect("%s/judge/results/all/"%(settings.SITE_URL))
    elif bot_id != None:
        try:
            bot = models.Submission.objects.get(id=bot_id)
            runs = bot.player1_runset.all() | bot.player2_runset.all()
            runs = runs.order_by('-timestamp')
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "No bot by that id exists")
            return HttpResponseRedirect("%s/judge/results/all/"%(settings.SITE_URL))
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

