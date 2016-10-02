__author__ = "codingMonkey"
__project__ = "ChessML"

import sqlite3 as lite
import sys
from dev2.step4 import DB_DIR, DB_FAST_DIR

def create_database():
    con = None
    con = lite.connect(DB_DIR)
    with con:
        cur = con.cursor()
        # cur.execute("CREATE TABLE Movements(Id TEXT, n INT, white INT, black INT, draw INT)")
        # INSERT INTO Cars VALUES(1,'Audi',52642)


# create table BOARDS(ID text, white INT, black INT, DRAW INT);
def insert_list_into_boards(list_of_LISTS):
    MAX_WRITE = 1000
    MIN = 0
    MAX = 0
    n = len(list_of_LISTS)
    chunks = int(n/MAX_WRITE)
    con = lite.connect(DB_DIR)
    print DB_DIR
    with con:
        c = con.cursor()
        for i in range(chunks):
            MIN = i*MAX_WRITE
            MAX = (i+1)*MAX_WRITE
            print ("\r %d %d"%(MIN, MAX)),
            c.executemany('insert into BOA values (?,?,?,?)', list_of_LISTS[MIN:MAX])
        c.executemany('insert into BOA values (?,?,?,?)', list_of_LISTS[MAX:])
        con.commit()
        # con.close()


def query():
    con = lite.connect(DB_DIR)

    with con:

        cur = con.cursor()
        cur.execute("select white, draw, black from boards where ID='END';")
        l = ["a"]
        rows = cur.fetchall()
        # print type(rows)
        # print rows
        for row in rows:
            print row

        l.extend(rows[0])

        print l


class QueryHandler(object):
    # con = None
    FIELDS  = "WHITE, DRAW, BLACK"

    def __init__(self, db_dir=DB_FAST_DIR):
        self.con = lite.connect(db_dir)
        self.cur = self.con.cursor()

    # def __del__(self):
    #     if self.con:
    #         self.con.close()

    @staticmethod
    def get_query_id(id):
        return "SELECT white, draw, black FROM BOARDS WHERE ID='%s';"%id

    @staticmethod
    def sum_results(l):
        l.append((0,0,0)) # to have something in the result, in case that we dont find anything
        return [sum(x) for x in zip(*l)]

    @staticmethod
    def get_query_in_ids(list_ids):
        ids_str = "'" + "','".join(list_ids) + "'"
        query = "SELECT %s FROM BOARDS WHERE ID IN (%s);"%(QueryHandler.FIELDS,ids_str)
        return query

    def get_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()


    # def


if __name__ == '__main__':
    query()
    pass