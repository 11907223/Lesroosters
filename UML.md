<div hidden>
@startuml FirstDiagram

object Schedule
Schedule : ScheduleSlots

object ScheduleSlot
ScheduleSlot : Activity

object Activity
Activity : Type
Activity : Course
Activity : Student

object Course
Course : Activities
Course : Students

object Student
Student : Courses
Student : Activities

ScheduleSlot -up-> Schedule
Activity -up-> ScheduleSlot
Activity <-down-> Course
Activity <-down-> Student
Course <-right-> Student


@enduml
</div>

![UMl Diagram](FirstDiagram.svg)