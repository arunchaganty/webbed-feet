import Task

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

