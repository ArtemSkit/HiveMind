# importing the flask and sqlalchemy for the project
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='./template')
db = SQLAlchemy(app)
