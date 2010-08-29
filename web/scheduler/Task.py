import threading
import gbl

# Tasks
class Task(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass

    def run(self):
        print "Ran Task"

class OthelloGame(Task):
    __executable = gbl.EXECUTABLE
    __so1 = ""
    __so2 = ""

    def __init__(self, player1, player2):
        self.__so1 = os.path.join(settings.MEDIA_ROOT, player1.data)
        self.__so2 = os.path.join(settings.MEDIA_ROOT, player2.data)
        Task.__init__(self)

    def run(self):
        args = [__executable, self.__so1, self.__so2]

        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = p.communicate()[0]

        return output, 'game.log'

