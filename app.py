from flask import Flask, session, render_template ,url_for
import os
from storage.postgresHelper import PostgresDBHelper
from storage.mongoHelper import MongoDBHelper

from flask import *

postgres_db = PostgresDBHelper()
mongo_db = MongoDBHelper()

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html') 

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/faculty/<uname>')
def faculty(uname):
  return render_template('faculty.html',name=uname)


@app.route('/register/<typeOfRegistration>')
def register(typeOfRegistration):
	return render_template('register.html', name = typeOfRegistration, name1 = None)

@app.route('/register_emp')
def register_emp():
	return render_template('register.html', name ='employee', name1 = None)

@app.route('/register_dep')
def register_dep():
	return render_template('register.html', name ='department', name1 = None)

@app.route('/log')
def log():
  return render_template('log.html')



@app.route('/special_faculty/<section>')
def special_faculty(section):
  return render_template('special_faculty.html',name=section)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			return render_template('show_info.html', message = 'Invalid Credentials. Please try again.')
        else:
            return render_template('admin.html' , name='success', error = error)
			
    return render_template('admin.html', error=error)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
	 return render_template('login.html' , name="")

@app.route('/verify', methods=['GET', 'POST'])
def verify():
	error = None
	if request.method == 'POST':
		result = postgres_db.getLoginDetails(email = request.form['email'])
		
		if result == None:	#result[4] is e-mail
			return render_template('show_info.html', message = "Please ask Admin to register you as a faculty.")
		else:
			if result[5] == request.form['password']:	#result[5] is Password
				url= "/profile/"+ str(result[4])
				print(url)
				return render_template('login.html',name= "success",profile_url = url)
			else:
				return render_template('show_info.html', message = "Invalid Credentials. Please Login Again.")

@app.route('/profile/<uemail>')
def profile(uemail):
		result = postgres_db.getLoginDetails(email = uemail)
		cv = mongo_db.getCV(result[0])
		print(cv)
		update_cv_url = '/cv/' + str(result[0])
		return render_template('faculty.html', name = "show_cv", emp_details = result, result = cv, update_cv_url = update_cv_url)

@app.route('/cv/<emp_id>')
def cv(emp_id):
	update_employee_cv_url = '/updateCV/' + str(emp_id)
	return render_template('register.html' , name='success', name1 = 'employee', emp_id = emp_id, 
			update_employee_cv_url = update_employee_cv_url, error = None)

@app.route('/updateCV/<emp_id>', methods = ['GET', 'POST'])
def updateCV(emp_id):
	error = False
	if request.method == 'POST':
		try:
			about_faculty = request.form['about_faculty']
			research_interests = request.form['research_interests']
			publications = request.form['publications']
			grants = request.form['grants']
			awards = request.form['awards']
			teaching_experience = request.form['teaching_experience']

			mongo_db.updateCV(emp_id, about_faculty, research_interests, publications, grants, awards, teaching_experience)

		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('show_info.html', message = "Your CV has been Successfully Updated")
	else:
		return render_template('show_info.html', message = "Could Not Update. See Terminal for more details")

@app.route('/registerDepartment', methods = ['GET', 'POST'])
def registerDepartment():
	error = False
	if request.method == 'POST':
		try:
			department = "Adarsh"
			department = request.form['dept_name']
			postgres_db.insertDepartment(name = department)
		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('show_info.html', message = "Department Registration Successful")
	else:
		return render_template('show_info.html', message = "Could Not Register. See Terminal for more details")

@app.route('/registerEmployee', methods=['GET', 'POST'])
def registerEmployee():
	error = False
	if request.method == 'POST':
		try:
			first_name = request.form['firstname']
			last_name = request.form['lastname']
			email = request.form['email']
			password = request.form['password']
			start_date = request.form['start_date']
			end_date = request.form['end_date']
			dept = request.form['department']
			username = first_name + '_' + start_date

			postgres_db.insertEmployee(username, first_name, last_name, email, password, start_date, end_date, dept = 1)
		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('show_info.html', message = "Employee Registration Successful")
	else:
		return render_template('show_info.html', message = "Could Not Register. See Terminal for more details")

@app.route('/update_hod', methods = ['GET', 'POST'])
def update_hod():
	error = False
	if request.method == 'POST':
		try: 
			department =  request.form['department']
			employee_id = request.form['id']
			
			result = postgres_db.getLoginDetails(id = employee_id)
			if(result == []):
				return render_template('show_info.html' , message = "Enter a valid Employee ID")

			postgres_db.update_hod_table(1, employee_id)
			 
		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('show_info.html' , message = "HOD was successfully updated.")
	else:
		return render_template('show_info.html' , message = "Could Not Update. See Terminal for more details")

@app.route('/update_dean', methods = ['GET', 'POST'])
def update_dean():
	error = False
	if request.method == 'POST':
		try: 
			department = request.form['section']
			employee_id = request.form['id']

			result = postgres_db.getLoginDetails(id = employee_id)
			if(result == []):
				return render_template('show_info.html' , message = "Enter a valid Employee ID")
			
			postgres_db.update_dean_table(1, employee_id)

		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('show_info.html' , message = "CC_Faculty was successfully updated.")
	else:
		return render_template('show_info.html' , message = "Could Not Update. See Terminal for more details")

@app.route('/apply_leave', methods = ['GET', 'POST'])
def apply_leave():
	error = False
	if request.method == 'POST':
		try: 
			  days=    request.form['days'] 
			  ##apply database action

		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('faculty.html' , name='success', error = error)
	else:
		return render_template('show_info.html', message = "Could Not Register. See Terminal for more details")
