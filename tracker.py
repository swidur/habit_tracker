import psycopg2
import datetime
from prettytable import PrettyTable

def get_activ_names():
    """Return all activities in dec order by hrs."""
    db = psycopg2.connect("dbname='habit_tracker' user='postgres' host='localhost' password='XXX'")
    c = db.cursor()
    c.execute("select distinct activ,duration,id  from loger order by duration desc;")
    rows = c.fetchall()
    tab = PrettyTable(['Hours', 'Name', 'ID'])
    for row in rows:
        names = row[0]
        hours = row[1]
        ids = row[2]
        tab.add_row([hours,names,ids])
    print tab
    db.close()


def add_activ(activity, duration):
    """add new activity"""

    db = psycopg2.connect("dbname='habit_tracker' user='postgres' host='localhost' password='XXX'")
    c = db.cursor()
    c.execute("insert into loger values ('{0}',{1},current_timestamp);".format(activity, duration))
    db.commit()
    db.close()


def rmv_activ(act_id):
    """remove activity"""
    db = psycopg2.connect("dbname='habit_tracker' user='postgres' host='localhost' password='XXX'")
    c = db.cursor()
    c.execute('select activ, duration, id from loger where id ={}'.format(act_id))
    deleted = []
    deleted = [i for i in c.fetchone()]
    c.execute("delete from loger where id={};".format(act_id))
    print ('Deletion successful!  Activity: "{}", hours: {}, ID: {}.'.format(deleted[0],deleted[1],deleted[2]))

    db.commit()
    db.close()

