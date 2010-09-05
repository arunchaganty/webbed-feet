# Wrapper to access a Task from the database.

import sqlite3
from datetime import datetime

class Bot:
    """Wrapper about a bot instance"""
    def __init__(self, conn, bot_id, team_id, timestamp, checksum, path, comments):
        self.bot_id = bot_id
        self.team_id = team_id
        self.timestamp = timestamp
        self.checksum = checksum
        self.path = path
        self.comments = comments

        self.__conn = conn 

    def __repr__(self):
        return "[Bot #%d]"%(self.bot_id)

    def __str__(self):
        return "Bot #%d"%(self.bot_id)
    
    def get_count(self):
        return self.__conn.get_count(self)

class BotDb:
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        return -1
    
    def all(self):
        """Get all the submitted bots"""
        pass

    def filter(self, **kwargs):
        """Get some of the submitted bots"""
        pass
    
    def get(self, id):
        """Get a submitted bot"""
        pass

    def get_count(self, bot = None):
        pass

    def add_run(self, bot1, bot2, score, timestamp):
        pass

class SQLiteBotDb(BotDb):
    def __init__(self, filename):
        self.__conn = sqlite3.Connection(filename)
        # HACK!
        self.__submissionTable = "judge_submission"
        self.__runTable = "judge_run"

    def __getitem__(self, idx):
        query = "SELECT * FROM %s ORDER BY timestamp DESC LIMIT %d,1"%(self.__submissionTable, idx)
        cursor = self.__conn.execute(query)
        b = cursor.fetchone()

        if b:
            return Bot(self,*b)
        else:
            return None

    def __iter__(self):
        query = "SELECT * FROM %s ORDER BY timestamp DESC"%(self.__submissionTable,)
        print query
        cursor = self.__conn.execute(query)

        for b in cursor:
            yield Bot(self,*b)

    def __len__(self):
        return self.get_count()

    # Interface functions

    def all(self):
        query = "SELECT * FROM %s"%(self.__submissionTable,)
        print query
        cursor = self.__conn.execute(query)

        return [ Bot(self,*b) for b in cursor ]

    def filter(self, **kwargs):
        query = "SELECT * FROM %s WHERE "%(self.__submissionTable,)
        for key,value in kwargs.items():
            query += "? = ? "%(key,value)
        print query
        cursor = self.__conn.execute(query)

        return [ Bot(self,*b) for b in cursor ]

    def get(self, id):
        query = "SELECT * FROM %s WHERE id = %d"%(self.__submissionTable, id)
        print query
        cursor = self.__conn.execute(query)
        b = cursor.fetchone()

        if b: 
            return Bot(self,*b)
        else: 
            return None

    def min(self):
        query = """SELECT bot.*, COUNT(run.id) as count FROM %s as bot,
        %s as run WHERE run.player1_id = bot.id OR run.player2_id =
        bot.id GROUP BY bot.id ORDER BY count LIMIT 1;"""%(self.__submissionTable, self.__runTable)
        print query
        cursor = self.__conn.execute(query)
        b = cursor.fetchone()
        b = b[:-1]

        if b: 
            return Bot(self,*b)
        else: 
            return None

    def get_count(self, bot = None):
        if bot == None:
            query = "SELECT COUNT(*) FROM %s"%(self.__submissionTable,)
            print query
            cursor = self.__conn.execute(query)
            e = cursor.fetchone()
            return e[0]
        else:
            query = "SELECT COUNT(*) FROM %s WHERE player1_id = %d or player2_id = %d"%(self.__runTable, bot.bot_id, bot.bot_id)
            print query
            cursor = self.__conn.execute(query)
            r = cursor.fetchone()
            return r[0]

    def add_run(self, bot1, bot2, score, timestamp = None):
        value_str = "(NULL, '%s', %d, %d, %d, '')"%(str(datetime.now()), bot1.bot_id, bot2.bot_id, score)
        query = "INSERT INTO %s VALUES %s"%(self.__runTable, value_str)
        print query
        cursor = self.__conn.execute(query)
        self.__conn.commit()
        return
        
