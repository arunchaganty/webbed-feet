# Task

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

    def is_alive(self):
        return False

    def join(self):
        pass

