from pymongo.errors import DuplicateKeyError
from datetime import datetime


def add_grade(db):
    date_str = input("Date (YYYY-MM-DD): ").strip()

    grade = {
        "grade_id": input("Grade ID: ").strip(),
        "student_id": input("Student ID: ").strip(),
        "course_id": input("Course ID: ").strip(),
        "grade_type": input("Grade type (exam/hw/lab/project): ").strip(),
        "grade_value": float(input("Grade value: ").strip()),
        "date": datetime.strptime(date_str, "%Y-%m-%d"),
        "comment": input("Comment: ").strip()
    }

    try:
        db.grades.insert_one(grade)
        print("Grade added successfully.")
    except DuplicateKeyError:
        print("Error: grade with this grade_id already exists.")
    except ValueError:
        print("Error: invalid date format.")
    except Exception as e:
        print(f"Error: {e}")


def list_all_grades(db):
    grades = db.grades.find({}, {"_id": 0})
    found = False

    for grade in grades:
        found = True
        print(grade)

    if not found:
        print("No grades found.")


def list_student_grades(db):
    student_id = input("Enter student_id: ").strip()
    grades = db.grades.find({"student_id": student_id}, {"_id": 0})

    found = False
    for grade in grades:
        found = True
        print(grade)

    if not found:
        print("No grades found for this student.")


def delete_grade(db):
    grade_id = input("Enter grade_id: ").strip()

    result = db.grades.delete_one({"grade_id": grade_id})

    if result.deleted_count:
        print("Grade deleted.")
    else:
        print("Grade not found.")