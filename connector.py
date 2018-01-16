import sqlite3 as lite


class Connector:
    def __init__(self):
        pass

    @staticmethod
    def connect():
        """Connect to the SQLite database. Returns a database connection."""
        return lite.connect('local.db')
