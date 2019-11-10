#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
import os
<<<<<<< HEAD

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
 
def connectPostgres(filename=os.path.abspath('config.ini'), section='postgresql'):
=======
from config import * 
 
def config(filename=os.path.abspath('config.ini'), section='postgresql'):
>>>>>>> 9c7bece71f2ffbf2209a58daaee51446bdaffdb7
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
<<<<<<< HEAD

    return db
=======
 
    return db 

 

>>>>>>> 9c7bece71f2ffbf2209a58daaee51446bdaffdb7
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
<<<<<<< HEAD

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
=======
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
>>>>>>> 9c7bece71f2ffbf2209a58daaee51446bdaffdb7
        # create a cursor
        cur = conn.cursor()
        
   # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
<<<<<<< HEAD

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        
=======
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
>>>>>>> 9c7bece71f2ffbf2209a58daaee51446bdaffdb7
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
<<<<<<< HEAD
            

=======
 
 
>>>>>>> 9c7bece71f2ffbf2209a58daaee51446bdaffdb7
if __name__ == '__main__':
    connect()