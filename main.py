from libraries.helpers.load_data import load_courses, load_students


if __name__ == "__main__":
    courses = load_courses()

    students = load_students(courses)

    for course in courses.values():
        print(course.name, course.students.keys())