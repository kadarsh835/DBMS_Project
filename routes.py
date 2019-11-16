from flask import Flask, render_template ,url_for
from flask import *  
import os
app = Flask(__name__)  
 
app = Flask(__name__)      
 
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/faculty')
def faculty():
  return render_template('faculty.html')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/log')
def log():
  return render_template('log.html')

@app.route('/profile')
def profile():
  return render_template('profile.html')

@app.route('/specialised_faculty')
def specialised_faculty():
  return render_template('specialised_faculty.html')


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

      #redirect(url_for())


 
if __name__ == '__main__':
  app.run(debug=True)