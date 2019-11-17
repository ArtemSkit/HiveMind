import uuid

from sqlalchemy import Column, String, Date, ForeignKey, SmallInteger, CHAR, Time, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Teacher(Base):
    __tablename__ = 'teacher'
    TeacherId = Column('teacherid',
                       UUID(as_uuid=True),
                       unique=True,
                       nullable=False,
                       primary_key=True,
                       default=uuid.uuid4())
    TeacherFName = Column('teacherfname', String(25), nullable=False)
    TeacherLName = Column('teacherlname', String(25), nullable=False)
    Department = Column('department', String(50), nullable=False)
    Email = Column('email', String(50), nullable=False)
    DOB = Column('dob', Date, nullable=False)
    TeacherAddress = Column('teacheraddress', String(50), nullable=False)
    Phone = Column('phone', String(13), nullable=True)
    PassHash = Column('passhash', String(64), nullable=False)
    Salt = Column('salt', String(50), nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from Teacher table.
        """
        return {
            'TeacherId': self.TeacherId,
            'TeacherFName': self.TeacherFName,
            'TeacherLName': self.TeacherLName,
            'Department': self.Department,
            'Email': self.Email,
            'DOB': self.DOB,
            'TeacherAddress': self.TeacherAddress,
            'Phone': self.Phone,
            'PassHash': self.PassHash,
            'Salt': self.Salt
        }


class DegreePlan(Base):
    __tablename__ = 'degreeplan'
    DegreePlanID = Column('degreeplanid',
                          UUID(as_uuid=True),
                          unique=True,
                          nullable=False,
                          primary_key=True,
                          default=uuid.uuid4())
    DegreeName = Column('degreename', String(50), nullable=False)
    Level = Column('level', CHAR, nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from DegreePlan table.
        """
        return {
            'DegreePlanID': self.DegreePlanID,
            'DegreeName': self.DegreeName,
            'Level': self.Level
        }


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


class Classes(Base):
    __tablename__ = 'classes'
    ClassId = Column('classid',
                     UUID(as_uuid=True),
                     unique=True,
                     nullable=False,
                     primary_key=True,
                     default=uuid.uuid4())
    CourseId = Column('courseid',
                      UUID(as_uuid=True),
                      ForeignKey(u'course.courseid'),
                      nullable=False)
    TeacherId = Column('teacherid',
                       UUID(as_uuid=True),
                       ForeignKey(u'teacher.teacherid'),
                       nullable=False)
    CRN = Column('crn', String(5), nullable=False)
    Campus = Column('campus', String(50), nullable=False)
    StartDate = Column('startdate', Date, nullable=False)
    ClassDays = Column('classdays', String(7), nullable=False)
    StartTime = Column('starttime', Time, nullable=False)
    EndTime = Column('endtime', Time, nullable=False)
    ClassLocation = Column('classlocation', String(50), nullable=True)
    Semester = Column('semester', String(10), nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from DegreePlan table.
        """
        return {
            'ClassId': self.ClassId,
            'CourseId': self.CourseId,
            'TeacherId': self.TeacherId,
            'CRN': self.CRN,
            'Campus': self.Campus,
            'StartDate': self.StartDate,
            'ClassDays': self.ClassDays,
            'StartTime': str(self.StartTime),
            'EndTime': str(self.EndTime),
            'ClassLocation': self.ClassLocation,
            'Semester': self.Semester
        }


class Student(Base):
    __tablename__ = 'student'
    StudentId = Column('studentid',
                       UUID(as_uuid=True),
                       unique=True,
                       nullable=False,
                       primary_key=True,
                       default=uuid.uuid4())
    StudentFName = Column('studentfname', String(25), nullable=False)
    StudentLName = Column('studentlname', String(25), nullable=False)
    DegreePlanID = Column('degreeplanid',
                          UUID(as_uuid=True),
                          ForeignKey(u'degreeplan.degreeplanid'),
                          nullable=False)
    Email = Column('email', String(50), nullable=False)
    DOB = Column('dob', Date, nullable=False)
    StudentAddress = Column('studentaddress', String(50), nullable=False)
    Phone = Column('phone', String(13), nullable=True)
    PassHash = Column('passhash', String(64), nullable=False)
    Salt = Column('salt', String(50), nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from Student table.
        """
        return {
            'StudentId': self.StudentId,
            'StudentFName': self.StudentFName,
            'StudentLName': self.StudentLName,
            'DegreePlanID': self.DegreePlanID,
            'Email': self.Email,
            'DOB': self.DOB,
            'StudentAddress': self.StudentAddress,
            'Phone': self.Phone,
            'PassHash': self.PassHash,
            'Salt': self.Salt
        }


class DegreeCourses(Base):
    __tablename__ = 'degreecourses'
    DegreePlanID = Column('degreeplanid',
                          UUID(as_uuid=True),
                          ForeignKey(u'degreeplan.degreeplanid'),
                          nullable=False,
                          primary_key=True)
    CourseId = Column('courseid',
                      UUID(as_uuid=True),
                      ForeignKey(u'course.courseid'),
                      nullable=False,
                      primary_key=True)

    @property
    def serialize(self):
        """
        :return: Serialized data from Student table.
        """
        return {'DegreePlanID': self.DegreePlanID, 'CourseId': self.CourseId}


class Registered(Base):
    __tablename__ = 'registered'
    RegisteredId = Column('registeredid',
                          UUID(as_uuid=True),
                          unique=True,
                          nullable=False,
                          primary_key=True,
                          default=uuid.uuid4())
    ClassId = Column('classid',
                     UUID(as_uuid=True),
                     ForeignKey(u'classes.classid'),
                     nullable=False)
    StudentId = Column('studentid',
                       UUID(as_uuid=True),
                       ForeignKey(u'student.studentid'),
                       nullable=False)
    Paid = Column('paid', Boolean, nullable=False)
    Complete = Column('complete', Boolean, nullable=False)
    LetterGrade = Column('lettergrade', String(1), nullable=True)
    NumberGrade = Column('numbergrade', Numeric, nullable=True)

    @property
    def serialize(self):
        """
        :return: Serialized data from DegreePlan table.
        """
        return {
            'RegisteredId': self.RegisteredId,
            'ClassId': self.ClassId,
            'StudentId': self.StudentId,
            'Paid': self.Paid,
            'Complete': self.Complete,
            'LetterGrade': self.LetterGrade,
            'NumberGrade': self.NumberGrade
        }


class Prerequisite(Base):
    __tablename__ = 'prerequisite'
    PrerequisiteId = Column('prerequisiteid',
                            UUID(as_uuid=True),
                            nullable=False,
                            primary_key=True,
                            default=uuid.uuid4())
    CourseId_Prerequisite = Column('courseid_prerequisite',
                                   UUID(as_uuid=True),
                                   ForeignKey(u'course.courseid'),
                                   nullable=False)
    CourseId = Column('courseid',
                      UUID(as_uuid=True),
                      ForeignKey(u'course.courseid'),
                      nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from Student table.
        """
        return {
            'PrerequisiteId': self.PrerequisiteId,
            'CourseId_Prerequisite': self.CourseId_Prerequisite,
            'CourseId': self.CourseId
        }


class Proposed(Base):
    __tablename__ = 'proposed'
    ProposedId = Column('proposedid',
                        UUID(as_uuid=True),
                        nullable=False,
                        primary_key=True,
                        default=uuid.uuid4())
    StudentId = Column('studentid',
                       UUID(as_uuid=True),
                       ForeignKey(u'student.studentid'),
                       nullable=False)
    CourseId = Column('courseid',
                      UUID(as_uuid=True),
                      ForeignKey(u'course.courseid'),
                      nullable=False)
    StartTime = Column('starttime', Time, nullable=False)
    EndTime = Column('endtime', Time, nullable=False)
    ProposedDays = Column('proposeddays', String(7), nullable=False)

    @property
    def serialize(self):
        """
        :return: Serialized data from Student table.
        """
        return {
            'ProposedId': self.ProposedId,
            'StudentId': self.StudentId,
            'CourseId': self.CourseId,
            'StartTime': str(self.StartTime),
            'EndTime': str(self.EndTime),
            'ProposedDays': self.ProposedDays
        }
