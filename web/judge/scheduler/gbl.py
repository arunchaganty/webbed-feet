# Contains the parameter settings for the Scheduler

import urllib
import pdb
import os
import subprocess

class GameError(Exception):
    pass

class DisqualificationError(GameError):
    def __init__(self, player):
        self.__player = player

    def __str__(self):
        return "[Error] %s disqualified"%(self.__player)

class TimeoutError(GameError):
    def __init__(self, player):
        self.__player = player

    def __str__(self):
        return "[Error] %s timed out"%(self.__player)

class CrashError(GameError):
    def __init__(self, player):
        self.__player = player

    def __str__(self):
        return "[Error] %s crashed"%(self.__player)

class UnknownError(GameError):
    def __init__(self):
        pass

    def __str__(self):
        return "[Error] Unknown Error"

def handleError(self, code, player1, player2):
    if code == "DQ1":
        raise DisqualificationError(player1)
    elif code == "DQ2":
        raise DisqualificationError(player2)
    elif code == "TO1":
        raise TimeoutError(player1)
    elif code == "TO2":
        raise TimeoutError(player2)
    elif code == "CR1":
        raise CrashError(player1)
    elif code == "CR2":
        raise CrashError(player2)
    elif code == "ERR":
        raise UnknownError()
    else:
        raise StandardError(code)

MAINLOOP_PERIOD = 5
PING_URL = urllib.basejoin("http://localhost:8000", "/home/ping/")
EXECUTABLE = "/home/teju/Projects/Desdemona/bin/Desdemona"
BASE_LOCATION="/home/teju/Projects/webbed-feet/web/media/"
CWD = "/home/teju/Projects/Desdemona/"

def processScore(score):
    # Add a constant offset
    if score < 0:
        score -= 50
    elif score > 0:
        score += 50
    return score
POST_RUN_SCORE = processScore

BUILDNEST = "/home/teju/Projects/automania/buildnest/bots/"
def processBinary(uploaded_file):
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
POST_SUBMISSION_HOOK = processBinary
POST_RUN_LOG = "game.log"

