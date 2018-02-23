import sqlite3 as lite
import logging

logging.basicConfig(filename='debug.log', format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='/%d-%m-%Y %H:%M:%S/', level=logging.DEBUG)


class Connector:
    def __init__(self, path):
        self.path = path
        self.default = 'default.db'

    def connect(self):
        """Connect to the SQLite database. Returns a database connection."""

        try:
            return lite.connect(self.path)

        except lite.OperationalError as op_er:
            info = 'Connector: {} at {}'.format(op_er, self.path)
            logging.warning(info)
            self.write_current_db(self.default)
            return lite.connect(self.default)

    def write_current_db(self, path):
        with open('current.txt', 'a+') as f:
            f.write('{}\n'.format(path))
