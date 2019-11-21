# Tutorial

## Installation

> 1.  Python installation
- [Python Download Documentation](https://www.python.org/downloads/)

> 2. Flask Installation
- [Flask Download Documentation](https://flask.palletsprojects.com/en/1.1.x/installation/)
    
> 3. Postgres Installation
- [Postgres Download](https://www.postgresql.org/download/)

> 4. pgAdmin Installation
- [pgAdmin Download](https://www.pgadmin.org/download/pgadmin-4-windows/)

## Crete database

1. Crete database <br/> ![Crete database](./Create_database.jpg)
2. Create ER model on [SqlDBM](https://sqldbm.com/) <br/> ![SqlDBM](./ER_model.jpg)
3. Export and combine scripts <br/> ![combine scripts](./Export.jpg)
4. Run scripts <br/> ![scripts](./Run_script.jpg)
5. Create Mock data on [mockaroo](https://mockaroo.com/) <br/> ![Mock data](./Mock.jpg)
6. Import Mock data <br/> ![Mock data](./Import_data.jpg)
7. Create sqlalchemy models <br/>
```Python
import uuid

from sqlalchemy import Column, String, Date, ForeignKey, SmallInteger, CHAR, Time, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Course(Base):
    __tablename__ = 'course'
    CourseId = Column('courseid',
                      UUID(as_uuid=True),
                      unique=True,
                      nullable=False,
                      primary_key=True,
                      default=uuid.uuid4())
    CourseName = Column('coursename', String(50), nullable=False)
    Credits = Column('credits', SmallInteger, nullable=False)
    CourseLevel = Column('courselevel', String(2), nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from DegreePlan table.
        """
        return {
            'CourseId': self.CourseId,
            'CourseName': self.CourseName,
            'Credits': self.Credits,
            'CourseLevel': self.CourseLevel
        }
```

## Local host configuration

> After installing Python Flask
1. Making folder
```Linux
mkdir <foldername>
cd <foldername>
touch flaskApp.py
```
2. Within same directory
```Linux
pip install Flask
```
3. Adding flask template code
> Open http://localhost:5000/ in your webbrowser, and “Hello World!” should appear.
```Py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
app.run()
```
4. Importing libraries & configuring routes.py file
```py
import sqlalchemy
from HiveMind import app
from flask import request, make_response, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import models as mod
# this will connect postgres to flask 
base = declarative_base()
db_uri = 'postgres://postgres:admin@localhost:5432/dbs_poroject'
db_eng = create_engine(db_uri)
ses = sessionmaker()
ses.configure(bind=db_eng)
ses = ses()
```

5. Creating URL Routes 
> Note: need to make different paths for each request
```py
from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "home!"

@app.route("/teachers")
@app.route("/teachers/")
def teachers():
    """

    :return: JSON result of querying for the all teachers.
    """
    try:
        teachers = ses.query(mod.Teacher).all()
        response = jsonify(Data=[b.serialize for b in teachers])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
        return make_response(jsonify(response), 405)

@app.route("/student")
@app.route("/student/")
def get_student():
    return "student"

@app.route("/students")
@app.route("/students/")
def get_students():
    return "students"

if __name__ == "__main__":
    app.run()
```

## Crete HTML page that requests data
![Page](./Front_end.jpg)





