import psycopg2
import os

class PostgresDBHelper:
    def __init__(self):
        self.connect()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        self.conn = None
        dbname = os.environ.get('DB_NAME', None)
        dbuser = os.environ.get('DB_USER', None)
        dbpass = os.environ.get('DB_PASS', None)
        dbhost = os.environ.get('DB_HOST', None)
        dbport = os.environ.get('DB_PORT', None)
        try:
            self.conn = psycopg2.connect(database=dbname, user = dbuser, password = dbpass,
                                        host = dbhost, port = dbport)
            
            # create a cursor
            cur = self.conn.cursor()
            
    # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)
            
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def createEmployee(self, username, name, email, password):
        cur = self.conn.cursor()

        err = False        
        try:
            cur.execute('INSERT INTO employee(username, name, email, passwd) VALUES (%s, %s, %s, %s)',
                            (username, name, email, password,))
        except:
            err = True

        cur.close()
        self.conn.commit()
        return err
    
                