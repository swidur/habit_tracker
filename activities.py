from prettytable import PrettyTable
from connector import Connector


class Activities:
    def __init__(self):
        self.connection = Connector.connect()

    def get_entries(self):
        """Returns a PrettyTable containing all entries ordered by act name, duration"""
        db = self.connection
        c = db.cursor()
        c.execute("select act, duration, act_id from loger order by act asc, duration asc")
        rows = c.fetchall()
        table = PrettyTable(['Hours', 'Name', 'ID'])
        for row in rows:
            names = row[0]
            hours = row[1]
            act_id = row[2]
            table.add_row([hours, names, act_id])
        return table

    def get_aggregated(self):
        """Returns a PrettyTable of distinct activities, summed up duration and entries count"""
        db = self.connection
        c = db.cursor()
        c.execute("select act, sum(duration) as sum, count(act) from loger group by act order by act asc, sum asc;")

        rows = c.fetchall()
        tab = PrettyTable(['Name', 'Hours', 'Count'])
        for row in rows:
            names = row[0]
            hours = row[1]
            counts = row[2]
            tab.add_row([names, hours, counts])
        return tab

    def add_act(self, Activity):
        """add new activity"""
        db = self.connection
        c = db.cursor()
        c.execute("insert into loger values ('{0}',{1},current_timestamp,NULL);".format(Activity.act, Activity.duration))
        db.commit()

    def del_by_id(self, act_id):
        """remove activity by act_id"""
        db = self.connection
        c = db.cursor()
        c.execute('select act, duration, act_id from loger where act_id ={}'.format(act_id))
        deleted = c.fetchone()
        if deleted:
            c.execute("delete from loger where act_id={};".format(act_id))
            print (
                'Deletion successful!  Activity: "{}", hours: {}, ID: {}.'.format(deleted[0], deleted[1], deleted[2]))
        else:
            print 'No such ID in DB!'
        db.commit()

    def del_by_name(self, act):
        """remove activity by act_id"""
        db = self.connection
        c = db.cursor()
        c.execute("select act, duration, act_id from loger where act ='{}'".format(act))
        deleted = c.fetchone()
        if deleted:
            c.execute("delete from loger where act='{}';".format(act))
            print ('Deletion successful! Activity: "{}" deleted.'.format(deleted[0]))
        else:
            print 'No such activity in DB!'
        db.commit()

    def close_connection(self):
        db = self.connection
        db.close()
