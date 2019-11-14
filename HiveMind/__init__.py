#importing the flask and sqlalchemy for the project 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder = './template')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://tmp/test.db'
db = SQLAlchemy(app)


from HiveMind import routes
