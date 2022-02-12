import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger()


class Database:
    """
    Node resposible for storing images in the database and retrieving them from it.
    :param dbpath: Full filepath to database .db file
    :type dbpath: str
    """
    def __init__(self, dbpath):
        self.dbpath = dbpath


    def get_connection(self):
        '''
        Connect to the database.
        :return: connection object used to interact with database
        '''
        con = None
        try:
            con = sqlite3.connect(self.dbpath)
            logger.debug("New connection to DB created.")
        except sqlite3.Error as err:
            logger.error("Error while creating connection to DB : %s", err)
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
        except sqlite3.Error as err:
            logger.error("Error while executing query %s : %s", query, err)
        finally:
            if con is not None:
                con.close()



    def get_data(self, query):
        '''
        Receive data from database.
        :param query: SQL query to execute (without commit)
        :type query: str
        :return: MultiDict containing requested data
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
        except sqlite3.Error as err:
            logger.error("Error while executing query %s : %s", query, err)
        finally:
            if con is not None:
                con.close()
        return result


    def image_exists(self, name, table):
        '''
        Check if image is already in database.
        :param name: Name of the image
        :type name: str
        :param table: Table where images are stored
        :type table: str
        :return: whether object exists (True) or not (False)
        '''
        logger.debug("Checking if image %s already exists...", name)
        con = None
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute('''SELECT * FROM {0} WHERE name = "{1}"'''.format(table, name))
            rows = cur.fetchall()
            if len(rows) > 0:
                return True
            return False
        except sqlite3.Error as err:
            logger.error("SQL Error while cheking if image %s exists : %s", name, err)
        except Exception as ex:
            logger.error("Error while checking if image %s exists : %s", name, ex)
        finally:
            if con is not None:
                con.close()



    def store_image(self, filepath, table, name = None):
        '''
        Store image inside of the database.
        :param filepath: Absolute path to the image file
        :type filepath: str
        :param table: Name of the table to store results in
        :type table: str
        :param name: This is the name of the picture after saving to db
        :type name: str
        '''
        con = None
        logger.debug("Storing image %s into table %s...", filepath, table)
        with open(filepath, 'rb') as file:
            try:
                path = filepath if name is None else name
                exists = self.image_exists(path, table)

                con = self.get_connection()
                cur = con.cursor()

                if exists:
                    logger.debug("Image %s already exists, overwritting...", path)
                    query = '''UPDATE {0} SET image = ? WHERE name = "{1}"'''.format(table, path)
                    data = (file.read(),)
                    cur.execute(query, data)
                    con.commit()
                else:
                    query = '''INSERT INTO {0} (date, name, image) VALUES (?, ?, ?)'''.format(table)
                    data = (datetime.now(), path, file.read())
                    cur.execute(query, data)
                    con.commit()

                logger.info("Image %s saved!", filepath)
            except sqlite3.Error as err:
                logger.error("SQL Error while adding image %s : %s", filepath, err)
            except Exception as ex:
                logger.error("Error while adding new image %s : %s", filepath, ex)
            finally:
                if con is not None:
                    con.close()


    def get_images(self, table):
        '''
        Get all image names from table.
        :param table: Table name to fetch images from
        :type table: str
        :return: List containing images' names
        '''
        logger.debug("Fetching images from table %s...", table)
        data = None
        try:
            rows = self.get_data('''SELECT name FROM {0}'''.format(table))
            data = [row[0] for row in rows]
            logger.debug("Images fetched.")
        except sqlite3.Error as err:
            logger.error("SQL Error while fetching images from table %s : %s", table, err)
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
        :return: requested image in Bytes format
        '''
        image = None
        logger.debug("Retrieving image %s from table %s...", filepath, table)
        try:
            image = self.get_data('''SELECT image FROM {0} WHERE name = '{1}' '''.format(table,
                                                                                         filepath))
            if len(image) > 0:
                image = image[0]
                logger.info("Image %s retrieved!", filepath)
            else:
                logger.error("Image %s does not exist.", filepath)
                image = None
        except sqlite3.Error as err:
            logger.error("SQL Error while fetching image %s : %s", filepath, err)
        except Exception as ex:
            logger.error("Error while fetching image %s : %s", filepath, ex)
        return image


    def remove_image(self, table, image):
        '''
        Remove the image from the database.
        Will do nothing if the image does not exist.
        :param table: Table where you store images
        :type table: str
        :param image: Name of the image to delete
        :type image: str
        '''
        logger.debug("Removing image %s...", image)
        removed = True
        try:
            exists = self.image_exists(image, table)
            if exists:
                self.commit_query('''DELETE FROM {0} WHERE name = '{1}' '''.format(table, image))
            else:
                logger.debug("Image %s does not exist, skipping removal...", image)
            logger.info("Image %s removed!", image)
            return removed
        except sqlite3.Error as err:
            removed = False
            logger.error("SQL Error while deleting image %s : %s", image, err)
            return removed
        except Exception as ex:
            removed = False
            logger.error("Exception while deleting image %s : %s", image, ex)
            return removed


    def get_state(self, table):
        '''
        Fetch current state of the plotter.
        Available states:
        * Idle - plotter ready to work
        * Busy - plotter already plotting
        * Error - unspecified error, assistance requested
        :param table: Table name where states are stored
        :type table: str
        :return: state of the plotter
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
        except sqlite3.Error as err:
            logger.error("SQL Error while fetching plotter state : %s", err)
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
                self.commit_query('''INSERT INTO {0} (id, state) VALUES (1, 'Idle')'''
                                  .format(table))
                logger.info("New state initialized!")
            else:
                logger.debug("State table already populated, skipping...")
        except sqlite3.Error as err:
            logger.error("SQL Error while initializing new state : %s", err)
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
            self.commit_query('''UPDATE {0} SET state = '{1}' WHERE id = 1'''.format(table,
                                                                                     new_state))
            logger.info("Plotter status changed to %s!", new_state)
        except sqlite3.Error as err:
            logger.error("SQL Error while changing state to %s : %s", new_state, err)
        except Exception as ex:
            logger.error("Exception while changing state to %s : %s", new_state, ex)
