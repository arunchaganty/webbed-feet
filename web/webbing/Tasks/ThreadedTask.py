import threading

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

    def is_alive(self):
        return self.isAlive()

