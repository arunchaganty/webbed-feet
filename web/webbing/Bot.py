# Wrapper to access a Task from the database.

import sqlite3
import MySQLdb

class Bot:
    """Wrapper about a bot's db instance"""
    def __init__(self, db, bot_id, team_id, timestamp, checksum, name, path, comments):
        self.bot_id = bot_id
        self.team_id = team_id
        self.timestamp = timestamp
        self.checksum = checksum
        self.name = name
        self.path = path
        self.comments = comments

        self.__db = db 

    def __repr__(self):
        return "[Bot #%d]"%(self.bot_id)

    def __str__(self):
        return "Bot #%d"%(self.bot_id)
    
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

class BotDb:
    """Abstract interface for a bot db"""

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

    def add_run(self, run):
        pass

class SQLBotDb(BotDb):
    def __init__(self, conn, submissionTable, runTable):
        self.conn = conn
        self.submissionTable = submissionTable
        self.runTable = runTable

    def execute(self, query):
        print query
        pass

    def all(self):
        """Get all the submitted bots"""

        query = "SELECT * FROM %s ORDER BY timestamp DESC"%(self.submissionTable,)
        cursor = self.execute(query)

        return [ Bot(self,*b) for b in cursor ]

    def filter(self, **kwargs):
        """Get some of the submitted bots"""
        query = "SELECT * FROM %s WHERE "%(self.submissionTable,)
        for key,value in kwargs.items():
            query += "? = ? "%(key,value)
        query += " ORDER BY timestamp DESC"
        cursor = self.execute(query)

        return [ Bot(self,*b) for b in cursor ]
    
    def get(self, id):
        """Get a submitted bot"""

        query = "SELECT * FROM %s WHERE id = %d"%(self.submissionTable, id)
        print query
        cursor = self.execute(query)
        b = cursor.fetchone()

        if b: 
            return Bot(self,*b)
        else: 
            return None

    def min(self):
        query = """SELECT bot.*, COUNT(run.id) as count FROM %s as bot,
        %s as run WHERE run.player1_id = bot.id OR run.player2_id =
        bot.id GROUP BY bot.id ORDER BY count LIMIT 1;"""%(self.submissionTable, self.runTable)
        cursor = self.execute(query)
        b = cursor.fetchone()

        if b and b[:-1]:
            b = b[:-1]
            return Bot(self,*b)
        else: 
            return None

    def getCount(self, bot = None):
        if bot == None:
            query = "SELECT COUNT(*) FROM %s"%(self.submissionTable,)
            cursor = self.execute(query)
            e = cursor.fetchone()
            return e[0]
        else:
            query = "SELECT COUNT(*) FROM %s WHERE player1_id = %d or player2_id = %d"%(self.runTable, bot.bot_id, bot.bot_id)
            cursor = self.execute(query)
            r = cursor.fetchone()
            return r[0]

    def insertRunQuery(self, run):
        value_str = "(NULL, '%s', %d, %d, %d, '%s', '%s')"%(run.timestamp, run.player1.bot_id, 
                run.player2.bot_id, run.score, run.status, run.game_data)
        query = "INSERT INTO %s VALUES %s"%(self.runTable, value_str)
        return query

class SQLiteBotDb(SQLBotDb):
    def __init__(self, filename):
        conn = sqlite3.Connection(filename)
        SQLBotDb.__init__(self, conn, "judge_submission", "judge_run")

    def execute(self, query):
        print query
        cursor = self.conn.execute(query)
        self.conn.commit()
        return cursor

class MySQLBotDb(SQLBotDb):
    def __init__(self, host, user, passwd, db):
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        SQLBotDb.__init__(self, conn, "judge_submission", "judge_run")

    def execute(self, query):
        print query
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return cursor

