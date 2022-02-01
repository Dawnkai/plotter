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
    def __init__(self, dbpath):
        self.dbpath = dbpath


    def get_connection(self):
        '''
        Connect to the database.
        '''
        con = None
        try:
            con = sqlite3.connect(self.dbpath)
            logger.debug("New connection to DB created.")
        except sqlite3.Error as e:
            logger.error("Error while creating connection to DB : %s", e)
        return con


    def commit_query(self, query):
        '''
        Execute SQL query that requires a commit on connection.
        Typically it's updating, inserting and creating data.
        :param query: SQL query to execute
        :type table_name: str
        '''
        con = None
        try:
            con = self.get_connection()
            cur = con.cursor()
            logger.debug("Executing commit query : %s...", query)
            cur.execute(query)
            con.commit()
            logger.debug("Query %s finished!", query)
        except sqlite3.Error as e:
            logger.error("Error while executing query %s : %s", query, e)
        finally:
            if con is not None:
                con.close()

    

    def get_data(self, query):
        '''
        Receive data from database.
        :param query: SQL query to execute (without commit)
        :type query: str
        '''
        con = None
        result = None
        try:
            con = self.get_connection()
            cur = con.cursor()
            logger.debug("Executing query : %s...", query)
            cur.execute(query)
            logger.debug("Query %s executed!", query)
            result = cur.fetchall()
        except sqlite3.Error as e:
            logger.error("Error while executing query %s : %s", query, e)
        finally:
            if con is not None:
                con.close()
        return result


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
            try:
                query = '''INSERT INTO {0} (date, name, image) VALUES (?, ?, ?)'''.format(table)
                con = self.get_connection()
                cur = con.cursor()
                data = (datetime.now(), filepath, file.read())
                cur.execute(query, data)
                con.commit()
                con.close()
                logger.info("Image %s saved!", filepath)
            except sqlite3.Error as e:
                logger.error("SQL Error while adding image %s : %s", filepath, e)
            except Exception as ex:
                logger.error("Error while adding new image %s : %s", filepath, ex)
    

    def get_images(self, table):
        '''
        Get all image names from table.
        :param table: Table name to fetch images from
        :type table: str
        '''
        logger.debug("Fetching images from table %s...", table)
        data = None
        try:
            rows = self.get_data('''SELECT name FROM {0}'''.format(table))
            data = [row[0] for row in rows]
            logger.debug("Images fetched.")
        except sqlite3.Error as e:
            logger.error("SQL Error while fetching images from table %s : %s", table, e)
        except Exception as ex:
            logger.error("Error while fetching images from table %s : %s", table, ex)
        return data


    def retrieve_image(self, table, filepath):
        '''
        Fetch image from the database.
        :param table: Table name to fetch image from
        :type table: str
        :param filepath: Absolute filepath of the image to fetch
        :type filepath: str
        '''
        image = None
        logger.debug("Retrieving image %s from table %s...", filepath, table)
        try:
            image = self.get_data('''SELECT image FROM {0} WHERE name = '{1}' '''.format(table, filepath))
            if len(image) > 0:
                image = image[0]
                logger.info("Image %s retrieved!", filepath)
            else:
                logger.error("Image %s does not exist.", filepath)
                image = None
        except sqlite3.Error as e:
            logger.error("SQL Error while fetching image %s : %s", filepath, e)
        except Exception as ex:
            logger.error("Error while fetching image %s : %s", filepath, ex)
        return image
    
    
    def get_state(self, table):
        '''
        Fetch current state of the plotter.
        Available states:
        * Idle - plotter ready to work
        * Busy - plotter already plotting
        * Error - unspecified error, assistance requested
        :param table: Table name where states are stored
        :type table: str
        '''
        state = "Error"
        logger.debug("Retrieving state of the plotter...")
        try:
            state = self.get_data('''SELECT * FROM {0}'''.format(table))
            if len(state) == 1:
                state = state[0][1]
                logger.info("State retrieved!")
            else:
                logger.error("More than one state is present, or none at all.")
                state = "Error"
        except sqlite3.Error as e:
            logger.error("SQL Error while fetching plotter state : %s", e)
        except Exception as ex:
            logger.error("Exception while fetching plotter state : %s", ex)
        return state


    def init_state(self, table):
        '''
        Create default state of plotter. Call only once.
        Will not create new status if one already exists.
        :param table: Table name where states are stored
        :type table: str
        '''
        logger.debug("Creating new plotter state...")
        try:
            state = self.get_data('''SELECT * FROM {0}'''.format(table))
            if len(state) == 0:
                self.commit_query('''INSERT INTO {0} (id, state) VALUES (1, 'Idle')'''.format(table))
                logger.info("New state initialized!")
            else:
                logger.debug("State table already populated, skipping...")
        except sqlite3.Error as e:
            logger.error("SQL Error while initializing new state : %s", e)
        except Exception as ex:
            logger.error("Exception while initializing new state : %s", ex)


    def change_state(self, table, new_state):
        '''
        Change the state of the plotter. If this fails,
        status will be changed to Error.
        :param table: Table name where states are stored
        :type table: str
        :param new_state: New state to set
        :type new_state: str
        '''
        logger.debug("Changing plotter state to %s...", new_state)
        try:
            self.commit_query('''UPDATE {0} SET state = '{1}' WHERE id = 1'''.format(table, new_state))
            logger.info("Plotter status changed to %s!", new_state)
        except sqlite3.Error as e:
            logger.error("SQL Error while changing state to %s : %s", new_state, e)
        except Exception as ex:
            logger.error("Exception while changing state to %s : %s", new_state, ex)
