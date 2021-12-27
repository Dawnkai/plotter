import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger()


class Database:
    """
    Node resposible for storing images in the database and retrieving them from it.
    :param con: Connection object used to connect to database with
    :param cur: Cursor obeject used to invoke commands on the database
    """
    def __init__(self, con = None, cur = None):
        self.con = con
        self.cur = cur


    def setup(self, dbpath):
        '''
        Connect to the database and create a cursor.
        :param dbpath: Absolute path to the database
        :type dbpath: str
        '''
        self.con = sqlite3.connect(dbpath)
        self.cur = self.con.cursor()


    def create_table(self, table_name):
        '''
        Create new table to store data in.
        Default data types in table are: (id, date, name, image).
        :param table_name: Table name to create
        :type table_name: str
        '''
        logger.debug("Creating new table %s...", table_name)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS %s
        (id NUMBER PRIMARY KEY, date DATE, name VARCHAR(30), image BLOB)''' % table_name)
        logger.info("Table %s created!", table_name)


    def store_image(self, filepath, table):
        '''
        Store image inside of the database.
        :param filepath: Absolute path to the image file
        :type filepath: str
        :param table: Name of the table to store results in
        :type table: str
        '''
        logger.debug("Storing image %s into table %s...", filepath, table)
        with open(filepath, 'rb') as file:
            self.con.execute('''INSERT INTO {0} (date, name, image)
            VALUES({1}, {2}, {3})'''.format(table, datetime.now(),
                                            filepath, sqlite3.Binary(file.read())))
            self.con.commit()
        logger.info("Image %s saved!", filepath)


    def retrieve_image(self, table, filepath):
        '''
        Fetch image from the database.
        :param table: Table name to fetch image from
        :type table: str
        :param filepath: Absolute filepath of the image to fetch
        :type filepath: str
        '''
        logger.debug("Retrieving image %s from table %s...", filepath, table)
        self.cur.execute('''SELECT image FROM {0} WHERE name = {1}'''.format(table, filepath))
        return self.cur.fetchone()
