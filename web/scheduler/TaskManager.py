# Task Manager

import settings
import subprocess
import os

# Tasks
class Task:
    def __init__(self):
        pass

class OthelloGame(Task):
    executable = "bin/Desdemona"
    so1 = ""
    so2 = ""

    def __init__(self, player1, player2):
        self.so1 = os.path.join(settings.MEDIA_ROOT, player1.data)
        self.so2 = os.path.join(settings.MEDIA_ROOT, player2.data)

    def run(self):
        args = [executable, self.so1, self.so2]

        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = p.communicate()[0]

        return output, 'game.log'

class TaskManager:
    def __init__(self):
        pass

class OthelloGameManager(TaskManager):
    """Creates a new Othello Game instance to be played"""

    def get(player1, player2):
        return OthelloGame(player1, player2)

