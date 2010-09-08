# Contains the parameter settings for the Scheduler

import urllib
import pdb
import os
import subprocess

MAINLOOP_PERIOD = 5
PING_URL = urllib.basejoin("http://localhost:8000", "/home/ping/")
EXECUTABLE = "/home/teju/Projects/Desdemona/bin/Desdemona"
BASE_LOCATION="/home/teju/Projects/webbed-feet/web/media/"
CWD = "/home/teju/Projects/Desdemona/"

def process_score(score):
    # Add a constant offset
    if score < 0:
        score -= 50
    elif score > 0:
        score += 50
    return score
POST_RUN_SCORE = process_score

BUILDNEST = "/home/teju/Projects/automania/buildnest/bots/"
def process_binary(uploaded_file):
    """Compile a C++ File"""

    uploaded_file.seek(0)
    data = uploaded_file.read()

    # Copy to the buildnest
    botFile = open(os.path.join(BUILDNEST, "bot.cpp"), "w")
    botFile.write(data)
    botFile.close()

    # cd to the directory and make
    p = subprocess.Popen(["make"], cwd=BUILDNEST)
    output = p.communicate()

    # 
    botSo = open(os.path.join(BUILDNEST, "bot.so"), "r")
    data = botSo.read()
    
    return data

# Judge settings
POST_SUBMISSION_HOOK = process_binary

