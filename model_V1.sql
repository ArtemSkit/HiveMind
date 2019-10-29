CREATE EXTENSION
IF NOT EXISTS "uuid-ossp";

CREATE TABLE Teacher
(
  TeacherId UUID NOT NULL DEFAULT uuid_generate_v1(),
  TeacherFName varchar(25) NOT NULL,
  TeacherLName varchar(25) NOT NULL,
  Department varchar(50) NOT NULL,
  Email varchar(50) NOT NULL,
  DOB date NOT NULL,
  TeacherAddress varchar(50) NOT NULL,
  Phone char(13) NULL,
  PassHash char(model.sql) NOT NULL,
  Salt varchar(50) NOT NULL
);

CREATE UNIQUE INDEX PK_Student_Teacher ON Teacher
(
 TeacherId
);

CREATE TABLE Student
(
  StudentId uuid NOT NULL DEFAULT uuid_generate_v1(),
  StudentFName varchar(25) NOT NULL,
  StudentLName varchar(25) NOT NULL,
  Major varchar(50) NOT NULL,
  Email varchar(50) NOT NULL,
  DOB date NOT NULL,
  StudentAddress varchar(50) NOT NULL,
  Phone char(13) NULL,
  PassHash char(64) NOT NULL,
  Salt varchar(50) NOT NULL
);

CREATE UNIQUE INDEX PK_Student ON Student
(
 StudentId
);

CREATE TABLE Course
(
  CourseId uuid NOT NULL DEFAULT uuid_generate_v1(),
  CourseName varchar(50) NOT NULL,
  Credits smallint NOT NULL,
  CourseLevel varchar(2) NOT NULL,
  Semester varchar(10) NOT NULL
);

CREATE UNIQUE INDEX PK_Course ON Course
(
 CourseId
);

CREATE TABLE Class
(
  ClassId uuid NOT NULL DEFAULT uuid_generate_v1(),
  CourseId uuid NOT NULL,
  TeacherId uuid NOT NULL,
  CRN varchar(5) NOT NULL,
  Campus varchar(50) NULL,
  StartDate date NOT NULL,
  ClassDays varchar(7) NOT NULL,
  StartTime time(6) NOT NULL,
  EndTime time(6) NOT NULL,
  ClassLocation varchar(50) NULL,
  Semester varchar(10) NOT NULL,
  CONSTRAINT FK_193 FOREIGN KEY ( CourseId ) REFERENCES Course ( CourseId ),
  CONSTRAINT FK_252 FOREIGN KEY ( TeacherId ) REFERENCES Teacher ( TeacherId )
);

CREATE UNIQUE INDEX PK_Class ON Class
(
 ClassId
);

CREATE INDEX fkIdx_193 ON Class
(
 CourseId
);

CREATE INDEX fkIdx_252 ON Class
(
 TeacherId
);

CREATE TABLE Takes
(
  StudentId uuid NOT NULL,
  CourseId uuid NOT NULL,
  Taken boolean NOT NULL,
  CONSTRAINT FK_196 FOREIGN KEY ( CourseId ) REFERENCES Course ( CourseId ),
  CONSTRAINT FK_258 FOREIGN KEY ( StudentId ) REFERENCES Student ( StudentId )
);

CREATE UNIQUE INDEX PK_table_157 ON Takes
(
 CourseId,
 StudentId
);

CREATE INDEX fkIdx_196 ON Takes
(
 CourseId
);

CREATE INDEX fkIdx_258 ON Takes
(
 StudentId
);

CREATE TABLE Prerequisite
(
  PrerequisiteId uuid NOT NULL DEFAULT uuid_generate_v1(),
  CourseId uuid NOT NULL,
  CourseId_Prerequisite uuid NOT NULL,
  CONSTRAINT FK_210 FOREIGN KEY ( CourseId ) REFERENCES Course ( CourseId ),
  CONSTRAINT FK_214 FOREIGN KEY ( CourseId_Prerequisite ) REFERENCES Course ( CourseId )
);

CREATE UNIQUE INDEX PK_Prerequisite ON Prerequisite
(
 PrerequisiteId
);

CREATE INDEX fkIdx_210 ON Prerequisite
(
 CourseId
);

CREATE INDEX fkIdx_214 ON Prerequisite
(
 CourseId_Prerequisite
);

CREATE TABLE Proposed
(
  ProposedId uuid NOT NULL DEFAULT uuid_generate_v1(),
  StudentId uuid NOT NULL,
  CourseId uuid NOT NULL,
  StartTime time(6) NOT NULL,
  EndTime time(6) NOT NULL,
  ProposedDays varchar(7) NOT NULL,
  CONSTRAINT FK_220 FOREIGN KEY ( CourseId ) REFERENCES Course ( CourseId ),
  CONSTRAINT FK_255 FOREIGN KEY ( StudentId ) REFERENCES Student ( StudentId )
);

CREATE UNIQUE INDEX PK_Proposed ON Proposed
(
 ProposedId
);

CREATE INDEX fkIdx_220 ON Proposed
(
 CourseId
);

CREATE INDEX fkIdx_255 ON Proposed
(
 StudentId
);