<div hidden>
@startuml FirstDiagram

class Schedule{
    days: dict[str: Day]
    -init_schedule() -> list[Days]
    day_schedule(day) -> list[slots] in day
    insert_activity(Day, Slot, Activity) -> bool. Modifies activity in place.
    as_list_of_dicts() -> dict representation of the Schedule.
}

class Day{
    day: str = Name of the day.
    slots : Dict OR list of slots.
    -init_day() : Fills the day with empty ScheduleSlots.
}

class Hall_slot{
    day : str
    time: str.
    room: str = Name of room.
    room_capacity : int = Max students inside a room.
    activity : Activity.
    is_empty() -> bool. Check if slot is occupied.
    fill() -> Set an active activity for the slot.
    check_capacity() -> bool. Check if capacity of room is not exceeded.
    as_dict() -> Return a dict representation of the slot.
}

class Activity{
    add_student(student) -> Inplace modification.
    course: Course = The course which the activity belongs to.
    category: str = The category of the activity. Options: lecture, tutorial or practical.
    capacity: int.
    students: list[Student].
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

Day -up-> Schedule
Hall_slot -up-> Day
Activity -up-> Hall_slot
Activity <-down-> Course
Activity <-down-> Student
Course <-right-> Student


@enduml
</div>

![UMl Diagram](FirstDiagram.svg)