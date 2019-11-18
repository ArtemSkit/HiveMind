import sqlalchemy
from HiveMind import app
from flask import request, make_response, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import models as mod

base = declarative_base()
db_uri = 'postgres://postgres:admin@localhost:5432/dbs_poroject'
db_eng = create_engine(db_uri)
ses = sessionmaker()
ses.configure(bind=db_eng)
ses = ses()

meta = sqlalchemy.MetaData(db_eng)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/teachers', methods=['GET'])
@app.route('/teachers/', methods=['GET'])
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


@app.route('/student', methods=['GET', 'POST'])
def get_student():
    """

    :return: JSON result of querying for all student's classes.
    """
    if request.method == 'POST':  #this block is only entered when the form is submitted
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


@app.route('/courses', methods=['GET'])
@app.route('/courses/', methods=['GET'])
def get_courses():
    """

    :return: JSON result of querying for the all courses.
    """
    try:
        courses = ses.query(mod.Course).all()
        response = jsonify(Data=[b.serialize for b in courses])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
        return make_response(jsonify(response), 405)


@app.route('/classes', methods=['GET'])
@app.route('/classes/', methods=['GET'])
def get_classes():
    """

    :return: JSON result of querying for the all classes.
    """
    try:
        classes = ses.query(mod.Classes).all()
        response = jsonify(Data=[b.serialize for b in classes])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
    return make_response(jsonify(response), 405)


@app.route('/degreecourses', methods=['GET'])
@app.route('/degreecourses/', methods=['GET'])
def get_degreecourses():
    """

    :return: JSON result of querying for the all degree courses.
    """
    try:
        degreecourses = ses.query(mod.DegreeCourses).all()
        response = jsonify(Data=[b.serialize for b in degreecourses])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
    return make_response(jsonify(response), 405)


@app.route('/registered', methods=['GET'])
@app.route('/registered/', methods=['GET'])
def get_registered():
    """

    :return: JSON result of querying for the all course registrations.
    """
    try:
        registered = ses.query(mod.Registered).all()
        response = jsonify(Data=[b.serialize for b in registered])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
    return make_response(jsonify(response), 405)


@app.route('/prerequisite', methods=['GET'])
@app.route('/prerequisite/', methods=['GET'])
def get_prerequisite():
    """

    :return: JSON result of querying for the all prerequisites.
    """
    try:
        prerequisites = ses.query(mod.Prerequisite).all()
        response = jsonify(Data=[b.serialize for b in prerequisites])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
    return make_response(jsonify(response), 405)


@app.route('/proposed', methods=['GET'])
@app.route('/proposed/', methods=['GET'])
def get_proposed():
    """

    :return: JSON result of querying for the all proposals.
    """
    try:
        proposals = ses.query(mod.Proposed).all()
        response = jsonify(Data=[b.serialize for b in proposals])
        return make_response(response, 201)
    except (SQLAlchemyError, DBAPIError) as e:
        print(e)
        response = {'status': "Failed", 'reason': e}
    return make_response(jsonify(response), 405)


@app.route('/proposed/add', methods=['POST'])
def add_proposed():
    """
    :return: Success or failure of insert into the Proposed table.
    """
    json_data = request.get_json(force=True)
    if not json_data:
        response = {'message': 'No input data provided'}
        return make_response(jsonify(response), 400)

    proposed = mod.Proposed(StudentId=json_data.get('StudentId'),
                            CourseId=json_data.get('CourseId'),
                            StartTime=json_data.get('StartTime'),
                            EndTime=json_data.get('EndTime'),
                            ProposedDays=json_data.get('ProposedDays'))
    ses.add(proposed)
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


if __name__ == '__main__':
    # CONFIGURATION
    app.debug = True
    app.run(host='localhost', port=5000)
