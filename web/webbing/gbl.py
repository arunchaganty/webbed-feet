# Contains the parameter settings for Webbing

import os
import urllib
import subprocess

# Daemon Properties
MAINLOOP_PERIOD = 5 # seconds
PING_URL = urllib.basejoin("http://localhost:8000", "/home/ping/")
BASE_LOCATION="/home/teju/Projects/webbed-feet/web/media/"

# Game Properties
CWD = "/home/teju/Projects/automania/prob1/"
EXECUTABLE = "/home/teju/Projects/automania/prob1/bin/snake"

# Judge settings
POST_SUBMISSION_HOOK = processBinary
POST_RUN_LOG = "game.log"
POST_RUN_LOG_PATH = "/home/teju/Projects/webbed-feet/web/media/logs/"


def processScore(score):
    # Add a constant offset
    if score < 0:
        score -= 50
    elif score > 0:
        score += 50
    return score
POST_RUN_SCORE = processScore
