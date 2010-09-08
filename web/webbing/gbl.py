# Contains the parameter settings for Webbing

import os
import urllib

# Daemon Properties
MAINLOOP_PERIOD = 5 # seconds
PING_URL = urllib.basejoin("http://localhost:8000", "/home/ping/")
BASE_LOCATION="/home/teju/Projects/webbed-feet/web/media/"

# Game Properties
GAME_CWD = "/home/teju/Projects/automania/prob1/"
EXECUTABLE = "/home/teju/Projects/automania/prob1/bin/snake"

# Judge settings
POST_RUN_LOG = "game_out.txt"

def processScore(score):
    if score.isdigit():
        score = int(score)
        # Add a constant offset of 50
        if score < 0:
            score -= 50
        elif score > 0:
            score += 50
        return score
    else:
        # Handle various error codes
        return 0
POST_RUN_HOOK = processScore

