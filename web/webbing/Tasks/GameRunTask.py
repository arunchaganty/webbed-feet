import gbl
from ThreadedTask import ThreadedTask
from RunUpdateTask import RunUpdateTask

class GameRunTask(ThreadedTask):
    """Run the game"""

    def __init__(self, game, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        ThreadedTask.__init__(self, str((player1, player2)))

    def run(self):
        run_data = self.game.runHook(self.player1, self.player2)
        self.taskManager.add_task(RunUpdateTask(run_data))

