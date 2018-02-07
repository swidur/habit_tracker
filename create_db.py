import sqlite3 as lite

con = None
try:
    con = lite.connect('local.db')
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS loger (act TEXT NOT NULL, duration INTEGER NOT NULL,date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,act_id INTEGER PRIMARY KEY);')


except lite.Error, e:

    print "Error %s:" % e.args[0]
