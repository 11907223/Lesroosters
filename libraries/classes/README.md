# Classes

This package includes several classes to store data to be used for schedule assignment in the project.
Activity, Course, Hall and Student are immmutable data designed for data storage. The Model class is a representation of a timetable and designed for manipulation through algorithms.


## Table of Contents

* [activity.py](#activity.py)
* [course.py](#course.py)
* [hall.py](#hall.py)
* [model.py](#model.py)
* [student.py](#student.py)

## [activity.py](/libraries/classes/activity.py)

The Activity Class is a datastructure which represents an activity. It contains information about the course from which the activity stems, the participating students in the activity, and the capacity available for the activity.

## [course.py](/libraries/classes//course.py)

The Course Class represent a specific course. It contains the name, activities in the course, and students enrolled in the course.

Methods of the course are:
* Adding a student
* Returning the number of activities
* Adding an activity

## [hall.py](/libraries/classes/hall.py)

The Hall Class is a datastructure containg information about a hall. It contains the name of the hall and the maximum capacity.

## [model.py](/libraries/classes/model.py)

The Model class represents a university timetable. It stores a _representation_ of activities and students which keeps it light weight. As an object designed to be manipulated, it contains a large number of methods for manipulation of information stored in the model.

Examples of methods (non-exhaustive) are:
* Adding an activity to an index in the timetable
* Swapping the activities stored at indices
* Calculating the number of penalty points of the timetable

## [student.py](/libraries/classes/student.py)

The Student class is a datastructure storing information about a student. It contains the index position of the student in the datafile, the student number of the student, their name and the courses they participate in.