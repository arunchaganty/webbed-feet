# Contains the parameter settings for the Scheduler

import urllib

def process_score(score):
    # Add a constant offset
    if score < 0:
        score -= 50
    elif score > 0:
        score += 50
    return score


MAINLOOP_PERIOD = 5
PING_URL = urllib.basejoin("http://localhost:8000", "/home/ping/")
EXECUTABLE = "/home/teju/Projects/Desdemona/bin/Desdemona"
BASE_LOCATION="/home/teju/Projects/webbed-feet/web/media/"
CWD = "/home/teju/Projects/Desdemona/"

POST_RUN_SCORE = process_score

