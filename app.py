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

@app.route('/profile')
def profile():
  return render_template('profile.html')

@app.route('/special_faculty/<section>')
def special_faculty(section):
  return render_template('special_faculty.html',name=section)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('admin.html' , name='success', error = error)
			
    return render_template('admin.html', error=error)


@app.route('/user/<uname>')
def user(uname):
      return render_template('message.html',name=uname)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('login.html' , name='success', error = error)
    return render_template('login.html', error=error)

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
		return render_template('register.html' , name='success', name1 = 'department', error = error)
	else:
		return "Could Not Register. See Terminal for more details"

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
		return render_template('register.html' , name='success', name1 = 'employee', error = error)
	else:
		return "Could Not Register. See Terminal for more details"

@app.route('/updateCV', methods = ['GET', 'POST'])
def updateCV():
	error = False
	if request.method == 'POST':
		try:
			about_faculty = request.form['about_faculty']
			research_interests = request.form['research_interests']
			publications = request.form['publications']
			grants = request.form['grants']
			awards = request.form['awards']
			teaching_experience = request.form['teaching_experience']

			mongo_db.updateCV(10, about_faculty, research_interests, publications, grants, awards, teaching_experience)

		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('register.html' , name='success', name1 = None, error = error)
	else:
		return "Could Not Update. See Terminal for more details"


@app.route('/update_hod', methods = ['GET', 'POST'])
def update_hod():
	error = False
	if request.method == 'POST':
		try: 
			department =  request.form['department']
			employee_id = request.form['id']
			firstname =   request.form['firstname']
			 ##apply database action
			 
		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('special_faculty.html' , name='success', error = error)
	else:
		return "Could Not Register. See Terminal for more details"

@app.route('/update_dean', methods = ['GET', 'POST'])
def update_dean():
	error = False
	if request.method == 'POST':
		try: 
			section =    request.form['section']
			employee_id = request.form['id']
			firstname =   request.form['firstname']
			  ##apply database action

		except Exception as e:
			error = True
			print(e)
	if not error:
		return render_template('special_faculty.html' , name='success', error = error)
	else:
		return "Could Not Register. See Terminal for more details"

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
		return "Could Not Register. See Terminal for more details"				
