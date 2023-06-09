from libraries.helpers.load_data import load_courses, load_students


if __name__ == "__main__":
    courses = load_courses()
    print(courses)

    students = load_students(courses)
    print(students)