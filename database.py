import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger()


class Database:
    def __init__(self, con = None, cur = None):
        self.con = con
        self.cur = cur


    def setup(self, dbpath):
        self.con = sqlite3.connect(dbpath)
        self.cur = self.con.cursor()
    

    def create_table(self, table_name):
        logger.debug("Creating new table {0}...", table_name)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS %s 
        (id NUMBER PRIMARY KEY, date DATE, name VARCHAR(30), image BLOB)''' % table_name)
        logger.info("Table {0} created!", table_name)


    def store_image(self, filepath, table):
        logger.debug("Storing image {0} into table {1}...".format(filepath, table))
        with open(filepath, 'rb') as f:
            self.con.execute('''INSERT INTO {0} (date, name, image)
            VALUES({1}, {2}, {3})'''.format(table, datetime.now(), filepath, sqlite3.Binary(f.read())))
            self.con.commit()
        logger.info("Image {0} saved!".format(filepath))
    

    def retrieve_image(self, table, filepath):
        logger.debug("Retrieving image {0} from table {1}...".format(filepath, table))
        self.cur.execute('''SELECT image FROM {0} WHERE name = {1}'''.format(table, filepath))
        return self.cur.fetchone()
