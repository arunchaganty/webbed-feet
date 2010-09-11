# Definitions of a task

import threading
import subprocess
import gbl

import random
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
    def __init__(self, queries):
        self.queries = queries
        Task.__init__(self, queries)

    def run(self):
        db = self.taskManager.db
        db.execute(self.queries)

    def start(self):
        self.run()

class GameRunTask(ThreadedTask):
    """Run the game"""

    def __init__(self, game, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        ThreadedTask.__init__(self)

    def run(self):
        run = self.game.runHook(self.player1, self.player2)

        db = self.game.db
        queries = db.getInsertRunQuery(run)
        self.taskManager.addTask(DBTask(queries))

