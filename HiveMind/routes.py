## routes where adding the locations and then 
## implenting the Models of the DB to the GUI

from flask import render_template, url_for, flash, redirect, request
from HiveMind import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

