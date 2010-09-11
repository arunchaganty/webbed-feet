#
# Database interface

import sqlite3
import MySQLdb


import Game
from Bot import Bot

class Db:
    def execute(self, query):
        raise NotImplemented()

class SQLiteDb(Db):
    def __init__(self, filename):
        self.conn = sqlite3.Connection(filename)

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

class MySQLDb(Db):
    def __init__(self, host, user, passwd, db):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

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

class WebbedFeetTable:
    def __init__(self, db, **kwargs):
        self.db = db
        self.tables = kwargs

    def getGames(self):
        query = "SELECT * FROM %s WHERE `active`=1"%(self.tables["game"])
        cursor = self.db.execute(query)

        return [ GameTable(self, *g) for g in cursor ]

class GameTable:
    def __init__(self, webbedFeetTable, game_id, name, cls, active):
        self.db = webbedFeetTable.db
        self.tables = webbedFeetTable.tables

        # Game properties
        self.game_id = game_id
        self.name = name
        self.cls = cls
        self.active = active

    def getClass(self):
        cls = getattr(Game, self.cls)
        cls.db = self
        return cls

    def listBots(self, order_by = None, reverse=False, limit=None):
        query = "SELECT * FROM %s WHERE `game_id` = %d AND `active`=1"%(
                self.tables["submission"], self.game_id,)

        if order_by: 
            query += " ORDER BY `%s`"%(order_by,)

            if reverse:
                query += " DESC"

        if limit != None:
            query += " LIMIT %d"%(limit)
        cursor = self.db.execute(query)

        return [ Bot(self,*b) for b in cursor ]

    def getBot(self, id):
        query = "SELECT * FROM %s WHERE id = %d"%(self.table["submission"], id)
        cursor = self.db.execute(query)
        b = cursor.fetchone()

        if b: 
            return Bot(self,*b)
        else: 
            return None

    def getCount(self):
        query = "SELECT COUNT(*) FROM %s"%(self.tables["submission"],)
        cursor = self.db.execute(query)
        e = cursor.fetchone()
        return e[0]

    def getInsertRunQuery(self, run):
        queries = []

        # Insert run
        value_str = "(NULL, '%s', %d, %d, %d, '%s', '%s')"%(run.timestamp, run.player1.id, 
                run.player2.id, run.score, run.status, run.game_data)
        query = "INSERT INTO %s VALUES %s"%(self.tables["run"], value_str)
        queries.append(query)

        # Update scores
        score = run.score

        if score > 0:
            player1, player2 = run.player1, run.player2
        else:
            player2, player1 = run.player1, run.player2

        count = player1.count + 1
        score = (score + player1.score * player1.count) / float(count)

        query = "UPDATE %s SET `score` = %f, `count` = %d WHERE `id` = %d"%(self.tables["submission"], score, count, player1.id)
        queries.append(query)

        if player2 != player1:
            count = player2.count + 1
            score = (0 + player2.score * player2.count) / float(count)

            query = "UPDATE %s SET `score` = %f, `count` = %d WHERE `id` = %d"%(self.tables["submission"], score, count, player2.id)
            queries.append(query)

        return queries

