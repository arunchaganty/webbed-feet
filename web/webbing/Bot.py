# Wrapper to access a Task from the database.

class Bot:
    """Wrapper about a bot's db instance"""

    def __init__(self, db, id, game_id, team_id, timestamp, sha1sum, name, data, comments, active, count, score):
        self.id = id
        self.game_id = game_id
        self.team_id = team_id
        self.timestamp = timestamp
        self.sha1sum = sha1sum
        self.name = name
        self.data = data
        self.comments = comments
        self.active = active
        self.count = count
        self.score = score

        self.__db = db 

    def __repr__(self):
        return "[Bot #%d]"%(self.id)

    def __str__(self):
        return "Bot #%d"%(self.id)
    
    def get_count(self):
        """Get number of plays"""
        return self.__db.get_count(self)

class Run:
    def __init__(self, timestamp, player1, player2, score, status, game_data):
        self.run_id = None
        self.timestamp = timestamp
        self.player1 = player1
        self.player2 = player2
        self.score = score
        self.status = status
        self.game_data = game_data

    def __repr__(self):
        return "[Run %s]"%(self.timestamp)

    def __str__(self):
        return self.__repr__()

