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

    def insertDepartment(self, id, name):
        cur = self.conn.cursor()
        err = False
        try:
            cur.execute(
                '''INSERT INTO department(name) 
                    VALUES (%s)''',
                        (name,)
            )
        except:
            err = True

        cur.close()
        self.conn.commit()
        return err
    
    def insertEmployee(self, username, first_name, last_name, email, password, start_date, end_date, dept):
        cur = self.conn.cursor()
        err = False        
        try:
            cur.execute('''INSERT INTO employee(user_name, first_name, last_name, email, passwd, start_date, end_date, dept) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %d)''',
                        (username, first_name, last_name, email, password, start_date, end_date, dept,))
        except:
            err = True

        cur.close()
        self.conn.commit()
        return err

    def insertHod(self, hod_id, start_date, end_date, dept):
        cur = self.conn.cursor()
        err = False
        try:
            cur.execute(
                '''INSERT INTO hod(hod_id, start_date, end_date, dept) 
                    VALUES (%d, %s, %s, %d)''',
                        (hod_id, start_date, end_date, dept)
            )
        except:
            err = True

        cur.close()
        self.conn.commit()
        return err
    
    def insertCC_faculty(self, cc_id, start_date, end_date, dept):
        cur = self.conn.cursor()
        err = False
        try:
            curr.execute(
                '''INSERT INTO cc_faculty(cc_id, start_date, end_date, dept) 
                    VALUES (%d, %s, %s, %d)''',
                        (cc_id, start_date, end_date, dept)
            )
        except:
            err = True
        cur.close()
        self.conn.commit()
        return err
    
    def inserDirector(self, dir_id, start_date, end_date):
        cur = self.conn.cursor()
        err = False
        try:
            curr.execute(
                '''INSERT INTO director(dir_id, start_date, end_date)
                    VALUES (%d, %s, %s)''',
                        (dir_id, start_date, end_date)
            )
        except:
            err = True
        cur.close()
        self.conn.commit()
        return err

    # def showLeaveApplicationStatus(self, leavesRemaining, nLeaveApplications, leaveApplicationStatus):
    #     cur = self.conn.connect()
    #     err = False
    #     try:
    #         cur.execute(

    #         )
    #     except:
    #         err = True
    #     cur.close()
    #     self.conn.commit()
    #     return err