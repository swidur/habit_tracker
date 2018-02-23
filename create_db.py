import sqlite3 as lite
from connector import Connector


def database(path):
    try:
        c = Connector(path)
        con = lite.connect(c.path)
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS loger (act TEXT NOT NULL, duration FLOAT NOT NULL,date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,act_id INTEGER PRIMARY KEY);')


    except lite.Error, e:

        print "Error %s:" % e.args[0]
