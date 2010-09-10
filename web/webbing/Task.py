# Definitions of a task

import threading
import subprocess
import gbl

import random
import shutil
import hashlib
import os
from datetime import datetime
import Bot

import errors

# Error
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


class Task():
    taskManager = None
    def __init__(self, *args):
        self.id = args

    def __repr__(self):
        return "[Task #%s]"%(self.id,)
    
    def __str__(self):
        return self.__repr__()

    def run(self):
        print "%s complete"%(str(self))

    def start(self):
        pass

    def isAlive(self):
        return False

    def join(self):
        pass

# Tasks
class ThreadedTask(threading.Thread):
    taskManager = None

    def __init__(self, *args):
        self.id = args
        threading.Thread.__init__(self)

    def __repr__(self):
        return "[ThreadedTask #%s]"%(self.id,)
    
    def __str__(self):
        return self.__repr__()

    def run(self):
        print "%s complete"%(str(self))

class DBTask(Task):
    """ Execute a DB query on the main thread """
    def __init__(self, query):
        self.__query = query
        Task.__init__(self, query)

    def run(self):
        db = self.taskManager.db
        db.execute(self.__query)

    def start(self):
        self.run()

class GameRunTask(ThreadedTask):
    """Run the game"""

    __executable = gbl.EXECUTABLE

    def __init__(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2
        ThreadedTask.__init__(self)

    def run(self):
        # Get arguments for the game
        so1 = os.path.join(gbl.BASE_LOCATION, self.__player1.path)
        so2 = os.path.join(gbl.BASE_LOCATION, self.__player2.path)
        args = [self.__executable, so1, so2]

        # Run the game
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=gbl.GAME_CWD)
        output = p.communicate()[0]
        ret = p.wait()

        # The hook takes care of output codes
        output = output.strip()
        score = gbl.POST_RUN_HOOK(output)
        if output.isdigit():
            status = "OK"
        # Else expect an error code
        elif output in ["DQ1", "DQ2", "TO1", "TO2", "CR1", "CR2", "ERR"]:
            status = output
        else:
            status = "ERR"

        log_path = ""
        try:
            # Also, save the game log file.
            if gbl.POST_RUN_LOG:
                log_in = os.path.join(gbl.GAME_CWD, gbl.POST_RUN_LOG)

                sha1sum = hashlib.sha1(open(log_in).read()).hexdigest()

                log_path = os.path.join("logs",sha1sum)
                log_out = os.path.join(gbl.BASE_LOCATION, log_path)
                # Copy the log file to the log location
                shutil.copy(log_in, log_out)
        except StandardError as e:
            print e
            log_path = ""

        run = Bot.Run(datetime.now(), self.__player1, self.__player2, score, status, log_path)
        db = self.taskManager.db
        query = db.insertRunQuery(run)
        self.taskManager.addTask(DBTask(query))

