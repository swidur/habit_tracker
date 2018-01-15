import psycopg2


class Connector:
    def __init__(self):
        pass

    @staticmethod
    def connect():
        """Connect to the PostgreSQL database.  Returns a database connection."""
        return psycopg2.connect("dbname='habit_tracker' user='postgres' host='localhost' password='XXXXX'")

