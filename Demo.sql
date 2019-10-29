Select *
from student
NATURAL JOIN degreecourses
NATURAL JOIN course  
where studentid = 'b388e54c-e3e0-11e9-9d67-df57c5d8096b' and courseid not in (
	Select courseid
  from registered
	NATURAL JOIN classes
	NATURAL JOIN course  
  where complete = true and studentid = 'b388e54c-e3e0-11e9-9d67-df57c5d8096b'
);

INSERT INTO public.proposed
  (
  studentid, courseid, starttime, endtime, proposeddays)
VALUES
  ( 'b388e54c-e3e0-11e9-9d67-df57c5d8096b', '5d0ac524-e3cb-11e9-8fa4-539e26619810', '09:00:00', '13:30:00', 'TR');

Select *
from proposed
natural join course ;