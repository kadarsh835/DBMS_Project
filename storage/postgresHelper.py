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
            print("insertDepartment !!")
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
            print("insertEmployee !!")
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
                        (hod_id, start_date, end_date, dept,)
            )
        except Exception as e:
            err = True
            print(e)
            print("insertHod !!")
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
                        (cc_id, start_date, end_date, dept,)
            )
        except Exception as e:
            err = True
            print(e)
            print("insertCC_faculty !!")
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
                        (dir_id, start_date, end_date,)
            )
        except Exception as e:
            err = True
            print(e)
            print("inserDirector !!")
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
            print("getLoginDetails !!")
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
                        current_time, None, department,)
            )
        except Exception as e:
            print(e)
            print("update_hod_table !!")
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
                '''INSERT INTO cc_faculty(cc_id, start_date, end_date, dept) VALUES (%s, %s, %s, %s)''', 
                        (emp_id, current_time, None, department,)
            )
        except Exception as e:
            print(e)
            print("update_dean_table !!")
        cur.close()
        self.conn.commit()
    
    def fetchEmployees(self):
        cur = self.conn.cursor()
        employees = []
        try:
            cur.execute('''SELECT * FROM employee''')
            employees = cur.fetchall()
        except Exception as e:
            print(e)
            print("fetchEmployees !!")
        cur.close()
        self.conn.commit()
        return employees
    
    def getEmployeeType(self, emp_id):
        cur = self.conn.cursor()
        try:
            cur.execute(
                '''SELECT dir_id FROM director WHERE dir_id = %s AND end_date is NULL''', (emp_id,)
            )
            director = cur.fetchone()
            if director is None:
                try:
                    cur.execute(
                        '''SELECT cc_id FROM cc_faculty WHERE cc_id = %s AND end_date is NULL''', (emp_id,)
                    )
                    cc = cur.fetchone()
                    if cc is None:
                        try:
                            cur.execute(
                                '''SELECT hod_id FROM hod WHERE hod_id = %s AND end_date is NULL''', (emp_id,)
                            )
                            hod = cur.fetchone()
                            if hod is None:
                                return "faculty"
                            else:
                                return "hod"
                        except Exception as e:
                            print(e)
                            return "could_not_determine"
                    else:
                        return "dean"
                except Exception as e:
                    print(e)
                    return "could_not_determine"
            else:
                return "director"
        except Exception as e:
            print(e)
            print("getemployeetype !!")
            return "could_not_determine"
    
    def getLastLeaveApplication(self, fac_id):
        cur = self.conn.cursor()
        try:
            cur.execute(
                '''SELECT * FROM leaves WHERE emp_id = %s''', (fac_id,)
            )
            leaveApplications = cur.fetchall()
            print('Leave Applications: ')
            print(leaveApplications)
            currentApplication = leaveApplications[len(leaveApplications) - 1]
            print('Current Applications: ')
            print(currentApplication)
            return currentApplication
        except Exception as e:
            print(e)
            print("getLastLeaveApplication !!")
            return []
    
    def applyForLeave(self, emp_id, start_date, no_of_days, final_review_by, employee_type, 
            hod_state = 0, dean_state = -1, director_state =-1):
        cur = self.conn.cursor()
        try:
            cur.execute(
            '''INSERT INTO leaves(emp_id, start_date, no_of_days, hod_state, dean_state, director_state, 
                        final_review_by, employee_type, employee_state) 
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (emp_id, start_date, no_of_days, 
                            hod_state, dean_state, director_state, final_review_by, employee_type, str(3),)
            )
        except Exception as e:
            print(e)
            print("applyForLeave !!")
        cur.close()
        self.conn.commit()
    
    def updateLeaveStatus(self, emp_id, status = 10):   #status = 10 to get application_no
        status = int(status)
        print(status)
        cur = self.conn.cursor()
        cur.execute(
            '''SELECT * FROM leaves WHERE emp_id = %s AND final_state = 'PROCESSING' ''', (emp_id,)
        )
        application = cur.fetchone()
        print(application)

        if status == 10:
            return application[0]

        comment_by = ''    

        if application[4] == 0:
            comment_by = 'hod'
        elif application[5] == 0:
            comment_by = 'dean'
        elif application[6] == 0:
            comment_by = 'director'
        else:
            comment_by = 'employee'

        try:
            if status == 1:
                cur.execute(
                        '''UPDATE leaves SET hod_state = -1, dean_state = -1, 
                                director_state = -1, employee_state = 0 WHERE emp_id = %s''', (emp_id,)
                    )
            
            elif status == 2:
                cur.execute(
                        '''UPDATE leaves SET hod_state = -1, dean_state = -1, 
                                director_state = -1, employee_state = -1, final_state = 'REJECTED' WHERE emp_id = %s''', (emp_id,)
                    )
            elif status == 3:
                
                if application[7] == 'hod' and application[4] == 0:
                    cur.execute(
                        '''UPDATE leaves SET hod_state = 3, final_state ='APPROVED' WHERE emp_id = %s''', (emp_id,)
                    )

                elif application[7] == 'dean' and application[5] == 0:
                    cur.execute(
                        '''UPDATE leaves SET dean_state = 3, final_state ='APPROVED' WHERE emp_id = %s''', (emp_id,)
                    )

                elif application[7] == 'director' and application[6] == 0:
                    cur.execute(
                        '''UPDATE leaves SET director_state = 3, final_state ='APPROVED' WHERE emp_id = %s''', (emp_id,)
                    )
                elif application[7] == 'director':
                    if application[5] == 0:
                        cur.execute(
                            '''UPDATE leaves SET hod_state = 3, dean_state = 3, director_state = 0 WHERE emp_id = %s''', (emp_id,)
                        )
                    elif application[4] == 0:
                        cur.execute(
                            '''UPDATE leaves SET hod_state = 3, dean_state = 0 WHERE emp_id = %s''', (emp_id,)
                        )
                    else:
                        cur.execute(
                            '''UPDATE leaves SET employee_state = 3, hod_state = 0 WHERE emp_id = %s''', (emp_id,)
                        )

                elif application[7] == 'dean':
                    if application[4] == 0:
                        cur.execute(
                            '''UPDATE leaves SET hod_state = 3, dean_state = 0 WHERE emp_id = %s''', (emp_id,)
                        )
                    else:
                        cur.execute(
                            '''UPDATE leaves SET employee_state = 3, hod_state = 0 WHERE emp_id = %s''', (emp_id,)
                        )
                elif application[7] == 'hod':
                    cur.execute(
                        '''UPDATE leaves SET employee_state = 3, final_state = 'APPROVED' WHERE emp_id = %s''', (emp_id,)
                    )
                else:
                    pass
        except Exception as e:
            print(e)
            print("updateLeaveStatus !!")
        cur.close()
        self.conn.commit()
        return application[0], comment_by

                

    def fetchApplications(self, cc_faculty, dept = None):
        cur = self.conn.cursor()
        applications = []
        try:
            if cc_faculty == 'hod':
                cur.execute(
                    '''SELECT * FROM leaves WHERE hod_state = 0'''
                )
                applications = cur.fetchall()
                print(applications)
                print('Department: ')
                print(dept)
                return_applications = []
                for application in applications:
                    emp_id = application[1]
                    employee = self.getLoginDetails(id = emp_id)
                    print(application)
                    print(employee[8])
                    print( dept )
                    if int(employee[8]) == int(dept):
                        print('TRUE')
                        return_applications.append(application)
                print(return_applications)
                return return_applications
        except Exception as e:
            print(e)
            print("fetchApplications !!")
        
        try:
            if cc_faculty == 'dean':
                cur.execute(
                    '''SELECT * FROM leaves WHERE dean_state = 0'''
                )
                applications = cur.fetchall()
                return applications
        except Exception as e:
            print(e)
            print("fetchApplications !!")
        
        try:
            if cc_faculty == 'director':
                cur.execute(
                    '''SELECT * FROM leaves WHERE director_state = 0'''
                )
                applications = cur.fetchall()
                return applications
        except Exception as e:
            print(e)
            print("fetchApplications !!")