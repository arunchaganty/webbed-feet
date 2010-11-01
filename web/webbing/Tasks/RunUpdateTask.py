import Task
from web.judge import models

class RunUpdateTask(Task.Task):
    """ Update the run_data (on main thread)"""
    def __init__(self, run_data):
        self.run_data = run_data
        Task.Task.__init__(self, str(run_data))

    def run(self):
        models.Run.add_run(self.run_data)

    def start(self):
        self.run()

