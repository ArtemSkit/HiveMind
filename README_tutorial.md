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
1. Making path <br />
![Screen Shot 2019-11-21 at 09 25 41](https://user-images.githubusercontent.com/22626710/69351413-e7864c80-0c40-11ea-8b16-6d4e98bec575.png)

```Linux
mkdir <foldername>
mkdir template
mkdir static
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
def get_teachers():
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
```
- Returning JSON result of querying for all students.
```py
@app.route('/students', methods=['GET'])
@app.route('/students/', methods=['GET'])
def get_students():
    """

    :return: JSON result of querying for the all students.
    """
    try:
        students = ses.query(mod.Student).all()
        response = jsonify(Data=[b.serialize for b in students])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
        return make_response(jsonify(response), 405)
```
- Student route to to query alll student's classes.
```py
@app.route('/student', methods=['GET', 'POST'])
def get_student():
    """

    :return: JSON result of querying for all student's classes.
    """
    if request.method == 'POST':
        print(request.form.get('studentId'))

        try:
            # students = ses.query(mod.Student).all()
            # mod.Student.StudentId == request.form.get('studentId'))
            degree_courses = ses.query(
                mod.Student, mod.DegreeCourses, mod.Course).join(
                    mod.DegreeCourses,
                    mod.DegreeCourses.DegreePlanID == mod.Student.DegreePlanID
                ).join(
                    mod.Course,
                    mod.DegreeCourses.CourseId == mod.Course.CourseId).filter(
                        mod.Student.StudentId == request.form.get(
                            'studentId')).all()
            courses = {'available': [], 'not-available': [], 'completed': []}
            for s, d, c in degree_courses:
                courses['not-available'].append(c)
            reg_courses = ses.query(
                mod.Registered, mod.Classes, mod.Course).join(
                    mod.Classes,
                    mod.Classes.ClassId == mod.Registered.ClassId).join(
                        mod.Course,
                        mod.Classes.CourseId == mod.Course.CourseId).filter(
                            mod.Registered.StudentId == request.form.get(
                                'studentId')).all()
            for s, d, c in reg_courses:
                print(s.Complete)
                if s.Complete:
                    courses['completed'].append(c)
            for course in courses['completed']:
                courses['not-available'].remove(course)
            for course in courses['not-available']:
                prereq_courses = ses.query(mod.Prerequisite).filter(
                    mod.Prerequisite.CourseId == course.CourseId).all()
                prereq_satisfied = 0
                for prereq in prereq_courses:
                    for completed_course in courses['completed']:
                        prereq_satisfied += 1
                        if prereq.CourseId_Prerequisite == completed_course.CourseId:
                            prereq_satisfied -= 1
                if prereq_satisfied == 0:
                    courses['available'].append(course)
            for course in courses['available']:
                courses['not-available'].remove(course)
            for key, val in courses.items():
                courses[key] = [b.serialize for b in courses[key]]
            response = jsonify(courses)
            return make_response(response, 201)
        except (SQLAlchemyError, DBAPIError) as e:
            print(e)
            response = {'status': "Failed", 'reason': e}
            return make_response(jsonify(response), 405)
```
- Query all degree plans 
```py
@app.route('/degreeplans', methods=['GET'])
@app.route('/degreeplans/', methods=['GET'])
def get_degreeplans():
    """

    :return: JSON result of querying for the all degree plans.
    """
    try:
        degreeplans = ses.query(mod.DegreePlan).all()
        response = jsonify(Data=[b.serialize for b in degreeplans])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
        return make_response(jsonify(response), 405)
```
- Success or failure of insert into degreee plans table.
```py
@app.route('/degreeplans/add', methods=['POST'])
def add_degreeplan():
    """
    :return: Success or failure of insert into the DegreePlans table.
    """
    json_data = request.get_json(force=True)
    if not json_data:
        response = {'message': 'No input data provided'}
        return make_response(jsonify(response), 400)

    degreeplan = mod.DegreePlan(DegreeName=json_data.get('DegreeName'),
                                Level=json_data.get('Level'))
    ses.add(degreeplan)
    ses.flush()

    try:
        ses.commit()
        response = {'status': "Success"}
        return make_response(jsonify(response), 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(str(e))
        ses.rollback()
        response = {'status': "Failed", 'reason': e}
        return make_response(jsonify(response), 405)
```

## Crete HTML page that requests data
![Page](./Front_end.jpg)
## Run
1. Clone the project
2. Go to the root directory
```Linux
cd HiveMind
```
3. run flask server
```Linux
python run.py
```
