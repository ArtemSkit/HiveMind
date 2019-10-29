CREATE EXTENSION
IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS Teacher CASCADE;
DROP TABLE IF EXISTS DegreePlan CASCADE;
DROP TABLE IF EXISTS Student CASCADE;
DROP TABLE IF EXISTS Course CASCADE;
DROP TABLE IF EXISTS DegreeCourses CASCADE;
DROP TABLE IF EXISTS Registered CASCADE;
DROP TABLE IF EXISTS class CASCADE;
DROP TABLE IF EXISTS Prerequisite CASCADE;
DROP TABLE IF EXISTS Proposed CASCADE;

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
  PassHash char(64) NOT NULL,
  Salt varchar(50) NOT NULL
);

CREATE UNIQUE INDEX PK_Student_Teacher ON Teacher
(
 TeacherId
);

CREATE TABLE DegreePlan
(
 DegreePlanID UUID NOT NULL DEFAULT uuid_generate_v1(),
 DegreeName   varchar(50) NOT NULL,
 Level        char(2) NOT NULL

);

CREATE UNIQUE INDEX PK_DegreePlan ON DegreePlan
(
 DegreePlanID
);

CREATE TABLE Student
(
 StudentId UUID NOT NULL DEFAULT uuid_generate_v1(),
 StudentFName   varchar(25) NOT NULL,
 StudentLName   varchar(25) NOT NULL,
 DegreePlanID   uuid NULL,
 Email          varchar(50) NOT NULL,
 DOB            date NOT NULL,
 StudentAddress varchar(50) NOT NULL,
 Phone          char(14) NULL,
 PassHash       char(64) NOT NULL,
 Salt           varchar(50) NOT NULL,
 CONSTRAINT FK_289 FOREIGN KEY ( DegreePlanID ) REFERENCES DegreePlan ( DegreePlanID )
);

CREATE UNIQUE INDEX PK_Student ON Student
(
 StudentId
);

CREATE INDEX fkIdx_289 ON Student
(
 DegreePlanID
);


CREATE TABLE Course
(
  CourseId uuid NOT NULL DEFAULT uuid_generate_v1(),
  CourseName varchar(50) NOT NULL,
  Credits smallint NOT NULL,
  CourseLevel varchar(2) NOT NULL
  );

CREATE UNIQUE INDEX PK_Course ON Course
(
 CourseId
);

CREATE TABLE Classes
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

CREATE UNIQUE INDEX PK_Classes ON Classes
(
 ClassId
);

CREATE INDEX fkIdx_193 ON Classes
(
 CourseId
);

CREATE INDEX fkIdx_252 ON Classes
(
 TeacherId
);



CREATE TABLE DegreeCourses
(
 DegreePlanID uuid NOT NULL,
 CourseId     uuid NOT NULL,
 CONSTRAINT FK_196 FOREIGN KEY ( CourseId ) REFERENCES Course ( CourseId ),
 CONSTRAINT FK_283 FOREIGN KEY ( DegreePlanID ) REFERENCES DegreePlan ( DegreePlanID )
);

CREATE UNIQUE INDEX PK_table_157 ON DegreeCourses
(
 CourseId,
 DegreePlanID
);

CREATE INDEX fkIdx_196 ON DegreeCourses
(
 CourseId
);

CREATE INDEX fkIdx_283 ON DegreeCourses
(
 DegreePlanID
);

CREATE TABLE Registered
(
 RegisteredId uuid NOT NULL DEFAULT uuid_generate_v1(),
 ClassId      uuid NOT NULL,
 StudentId    uuid NOT NULL,
 Paid         boolean NOT NULL,
 Complete    boolean NOT NULL,
 LetterGrade  char(1) NULL,
 NumberGrade  numeric NULL,
 CONSTRAINT FK_268 FOREIGN KEY ( ClassId ) REFERENCES Classes ( ClassId ),
 CONSTRAINT FK_271 FOREIGN KEY ( StudentId ) REFERENCES Student ( StudentId )
);

CREATE UNIQUE INDEX PK_Registered ON Registered
(
 RegisteredId
);

CREATE INDEX fkIdx_268 ON Registered
(
 ClassId
);

CREATE INDEX fkIdx_271 ON Registered
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