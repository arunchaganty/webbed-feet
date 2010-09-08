# Definitions of a task

import threading
import subprocess
import gbl

import random
import shutil
import hashlib
import os

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

class OthelloGame(ThreadedTask):
    __executable = gbl.EXECUTABLE

    def __init__(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2
        ThreadedTask.__init__(self)

    def run(self):
        so1 = os.path.join(gbl.BASE_LOCATION, self.__player1.path)
        so2 = os.path.join(gbl.BASE_LOCATION, self.__player2.path)
        args = [self.__executable, so1, so2]

        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=gbl.CWD)
        output = p.communicate()[0]
        # Post-process scores
        # Expect output to be one number, the score
        try:
            int(output)
        except ValueError:
            try:
                gbl.handleError(output, player1, player2)
            except GameError as e:
                score = gbl.POST_RUN_SCORE(int(output))

        # Also, save the game log file.
        log_path = None
        if gbl.POST_RUN_LOG:
            log_file = open(gbl.POST_RUN_LOG, "r")
            sha1sum = hashlib.sha1(data.read()).hexdigest()
            log_path = os.path.join(gbl.POST_RUN_LOG_PATH,sha1sum))
            shutil.copy(gbl.POST_RUN_LOG, log_path)

        db = self.taskManager.db
        query = db.addRun(self.__player1, self.__player2, score, log_path)
        self.taskManager.addTask(DBTask(query))

