import sqlite3 as lite


class Connector:
    def __init__(self, path):
        self.path = path

    def connect(self):
        """Connect to the SQLite database. Returns a database connection."""
        return lite.connect(self.path)
