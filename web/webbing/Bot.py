# Wrapper to access a Task from the database.

import sqlite3
import MySQLdb

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

        query = "SELECT * FROM %s WHERE `active`=1 ORDER BY timestamp DESC"%(self.submissionTable,)
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
            query = "SELECT COUNT(*) FROM %s WHERE player1_id = %d or player2_id = %d"%(self.runTable, bot.id, bot.id)
            cursor = self.execute(query)
            r = cursor.fetchone()
            return r[0]

    def insertRunQuery(self, run):
        value_str = "(NULL, '%s', %d, %d, %d, '%s', '%s')"%(run.timestamp, run.player1.id, 
                run.player2.id, run.score, run.status, run.game_data)
        query = "INSERT INTO %s VALUES %s"%(self.runTable, value_str)
        return query

    def updateScoreQuery(self, run):
        """ Update bot scores """
        score = run.score

        if score > 0:
            player1, player2 = run.player1, run.player2
        else:
            player2, player1 = run.player1, run.player2

        count = player1.count + 1

        score = (score + player1.score * player1.count) / float(count)
        query1 = "UPDATE %s SET `score` = %f, `count` = %d WHERE `id` = %d"%(self.submissionTable, score, count, player1.id)

        count = player2.count + 1
        score = (0 + player2.score * player2.count) / float(count)

        query2 = "UPDATE %s SET `score` = %f, `count` = %d WHERE `id` = %d"%(self.submissionTable, score, count, player2.id)

        if player1 == player2:
            return (query1,)
        else:
            return query1, query2

        
class SQLiteBotDb(SQLBotDb):
    def __init__(self, filename):
        conn = sqlite3.Connection(filename)
        SQLBotDb.__init__(self, conn, "judge_submission", "judge_run")

    def execute(self, query):
        print query
        # Handle lists
        if type(query) == list:
            for q in query:
                cursor = self.conn.execute(q)
        else:
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
        # Handle lists
        if type(query) == list:
            for q in query:
                cursor.execute(q)
                self.conn.commit()
        else:
            cursor.execute(query)
            self.conn.commit()
        return cursor

