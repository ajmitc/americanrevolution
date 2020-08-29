from datastore.datastore import DataStore
import sqlite3
from sqlite3 import Error
import traceback
import logging


class SQLiteDataStore(DataStore):
    def __init__(self):
        self.logger = logging.getLogger("server.SQLiteDataStore")
        self.db_file = "amrev.sqlite"
        self.conn = None

    def connect(self):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.logger.info("Connecting to DB File")
            self.conn = sqlite3.connect(self.db_file)
            return True
        except Error as e:
            self.logger.error(traceback.format_exc())
        return False

    def query(self, statement, values=None):
        if self.conn is None:
            if not self.connect():
                return False
        try:
            c = self.conn.cursor()
            c.execute(statement, values)
            rows = c.fetchall()
            return rows
        except Error as e:
            self.logger.error(traceback.format_exc())

    def execute(self, statement, values=None):
        if self.conn is None:
            if not self.connect():
                return False
        try:
            c = self.conn.cursor()
            c.execute(statement, values)
            self.conn.commit()
            return c.lastrowid
        except Error as e:
            self.logger.error(traceback.format_exc())

    def close(self):
        if self.conn:
            self.logger.info("Closing DB connection")
            self.conn.close()

    def install(self, filepath):
        if self.conn is None:
            if not self.connect():
                return False
        with open(filepath, 'r') as f:
            contents = f.read()
            try:
                c = self.conn.cursor()
                c.execute(contents)
            except Error as e:
                self.logger.error(traceback.format_exc())
