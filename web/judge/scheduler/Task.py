# Definitions of a task

import threading
import gbl

import random

BASE_LOCATION="/home/aditya/teju/"

class Task():
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
    def __init__(self, *args):
        self.id = args
        threading.Thread.__init__(self)

    def __repr__(self):
        return "[ThreadedTask #%s]"%(self.id,)
    
    def __str__(self):
        return self.__repr__()

    def run(self):
        print "%s complete"%(str(self))

class DBTestTask(Task):
    def __init__(self, db, player1, player2):
        self.__db = db
        self.__player1 = player1
        self.__player2 = player2
        Task.__init__(self, player1, player2)

    def run(self):
        self.__db.add_run(self.__player1, self.__player2, random.randint(-100,100))

    def start(self):
        self.run()

class OthelloGame(ThreadedTask):
    __executable = gbl.EXECUTABLE
    __so1 = ""
    __so2 = ""

    def __init__(self, player1, player2):
        self.__so1 = os.path.join(BASE_LOCATION, player1.data)
        self.__so2 = os.path.join(BASE_LOCATION, player2.data)
        Task.__init__(self)

    def run(self):
        args = [__executable, self.__so1, self.__so2]

        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = p.communicate()[0]

        return output, 'game.log'

