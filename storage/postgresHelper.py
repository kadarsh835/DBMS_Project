import psycopg2
import time
from datetime import datetime
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

    def insertDepartment(self, name):
        cur = self.conn.cursor()
        err = False
        print('Inside insertDepartment')
        try:
            print('Name: {0}' .format(name))
            cur.execute(
                '''INSERT INTO department(name) 
                    VALUES (%s)''',
                        (name,))
        except Exception as e:
            err = True
            print(e)

        cur.close()
        self.conn.commit()
        if not err:
            return "Department Inserted"
        else:
            return "Insert Department Failed"
    
    def insertEmployee(self, username, first_name, last_name, email, password, start_date, end_date, dept):
        cur = self.conn.cursor()
        err = False
        try:
            cur.execute('''INSERT INTO employee(user_name, first_name, last_name, email, passwd, start_date, end_date, dept) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                        (username, first_name, last_name, email, password, start_date, end_date, int(dept),))
        except Exception as e:
            err = True
            print(e)

        cur.close()
        self.conn.commit()
        return err

    def insertHod(self, hod_id, start_date, end_date, dept):
        cur = self.conn.cursor()
        err = False
        try:
            cur.execute(
                '''INSERT INTO hod(hod_id, start_date, end_date, dept) 
                    VALUES (%d, %s, %s, %s)''',
                        (hod_id, start_date, end_date, dept)
            )
        except Exception as e:
            err = True
            print(e)

        cur.close()
        self.conn.commit()
        return err
    
    def insertCC_faculty(self, cc_id, start_date, end_date, dept):
        cur = self.conn.cursor()
        err = False
        try:
            cur.execute(
                '''INSERT INTO cc_faculty(cc_id, start_date, end_date, dept) 
                    VALUES (%d, %s, %s, %s)''',
                        (cc_id, start_date, end_date, dept)
            )
        except Exception as e:
            err = True
            print(e)
        cur.close()
        self.conn.commit()
        return err
    
    def inserDirector(self, dir_id, start_date, end_date):
        cur = self.conn.cursor()
        err = False
        try:
            cur.execute(
                '''INSERT INTO director(dir_id, start_date, end_date)
                    VALUES (%d, %s, %s)''',
                        (dir_id, start_date, end_date)
            )
        except Exception as e:
            err = True
            print(e)
        cur.close()
        self.conn.commit()
        return err

    def getLoginDetails(self, email = None, id = None):
        cur = self.conn.cursor()
        result = None
        try:
            if id is None:
                cur.execute(
                    '''SELECT * FROM employee WHERE email = %s''', (email,)
                )
                result = cur.fetchone()
            else:
                cur.execute(
                    '''SELECT * FROM employee WHERE emp_id = %s''', (id,)
                )
                result = cur.fetchone()
            print(result)
            return result
        except Exception as e:
            print(e)
            return result
        cur.close()
        self.conn.commit()
    
    def update_hod_table(self, department, emp_id):
        cur = self.conn.cursor()
        try:
            current_time = time.time()
            current_time = datetime.fromtimestamp(current_time)
            print('Current Time')
            print(current_time)
            cur.execute(
                '''UPDATE hod SET end_date = %s WHERE dept = %s AND end_date is NULL''', ( current_time, department,)
            )
            cur.execute(
                '''INSERT INTO hod(hod_id, start_date, end_date, dept) VALUES (%s, %s, %s, %s)''', (emp_id, 
                        current_time, None, department)
            )
        except Exception as e:
            print(e)
        cur.close()
        self.conn.commit()
    
    def update_dean_table(self, department, emp_id):
        cur = self.conn.cursor()
        try:
            current_time = time.time()
            current_time = datetime.fromtimestamp(current_time)
            print('Current Time')
            print(current_time)
            cur.execute(
                '''UPDATE cc_faculty SET end_date = %s WHERE dept = %s AND end_date is NULL''', ( current_time, department,)
            )
            cur.execute(
                '''INSERT INTO cc_faculty(hod_id, start_date, end_date, dept) VALUES (%s, %s, %s, %s)''', 
                        (emp_id, current_time, None, department)
            )
        except Exception as e:
            print(e)
        cur.close()
        self.conn.commit()
    
    # def getHighestHeirarchy(self, emp_id):
    #     cur = self.con.cursor()
    #     try: