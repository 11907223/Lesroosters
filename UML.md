# UML Diagram

<div hidden>
@startuml
'Change only this value depending of the number of @startuml/@enduml on the full file
'https://forum.plantuml.net/13673/make-multiple-%40startuml%40enduml-blocks-file-generate-diagram
!$max=2
!$i=1
label l [
!while $i < $max+1
  {{
  !include %filename()!$i
  }}
  !$i = $i +1
!endwhile
]
@enduml

@startuml FirstDiagram

class Activity{
    add_student(student) -> Inplace modification.
    course: Course = The course which the activity belongs to.
    category: str = The category of the activity. Options: lecture, tutorial or practical.
    capacity: int.
    students: dict[str, Student].
}

class Course{
    number_of_activities() -> int.
    activities() -> list(Activities).
    add_student(Student) -> inplace modification.
    name: str.
    lectures: list[Activity].
    tutorials: list[Activity].
    practicals: list[Activity].
    max_tutorials_capacity: int.
    max_practical_capacity: int.
    expected: int.
}

class Student{
    add_course(course) -> inplace modification.
    index: int = Index of student in file.
    first_name: str.
    last_name: str.
    student_number: int.
    courses: list[Course].
}

Activity <-down-> Course
Activity <-down-> Student
Course <-right-> Student


@enduml

@startuml ModelDiagram

object Model{
    {field} index : int = Maps a unique index to a day-timeslot-hall combination ranging from 0 to 144 
        ((4 timeslots * 7 rooms + 1 evening slot) * 5 days).
    activity : str = string representation of the Activity object.
}

object Activity_participant_list{
    activity : str = string representation of the Activity object.
    student : str = string representation of the Student object. Based on their index number.
}

Model <- Activity_participant_list

@enduml

</div>

![UML Diagram](FirstDiagram.svg)
![](ModelDiagram.svg)