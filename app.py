from flask import Flask, session, render_template
import os

from storage.postgresHelper import PostgresDBHelper

db = PostgresDBHelper()

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

