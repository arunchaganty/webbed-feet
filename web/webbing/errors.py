"""
Defines the various errors that can be handled.
"""

class GameError(StandardError):
    def __init__(self, player, msg=""):
        self.player = player
        self.msg = msg

class DisqualificationError(GameError):
    def __init__(self, player, msg=""):
        GameError.__init__(self,player,msg)

    def __str__(self):
        val = "[Error] %s disqualified."%(self.player)
        if self.msg:
            val += "\n%s"%(self.msg)
        return val

class TimeoutError(GameError):
    def __init__(self, player, msg):
        GameError.__init__(self,player,msg)

    def __str__(self):
        val = "[Error] % timed out."%(self.player)
        if self.msg:
            val += "\n%s"%(self.msg)
        return val

class CrashError(GameError):
    def __init__(self, player, msg):
        GameError.__init__(self,player,msg)

    def __str__(self):
        val = "[Error] % crashed."%(self.player)
        if self.msg:
            val += "\n%s"%(self.msg)
        return val

class UnknownError(GameError):
    def __init__(self, msg):
        GameError.__init__(self, None,msg)

    def __str__(self):
        val = "[Error] Unknown Error."
        if self.msg:
            val += "\n%s"%(self.msg)
        return val

class BuildError(GameError):
    def __init__(self, msg):
        GameError.__init__(self, None, msg)

    def __str__(self):
        val = "[Error] Build Error."
        if self.msg:
            val += "\n%s"%(self.msg)
        return val


