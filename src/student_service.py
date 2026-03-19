from pymongo.errors import DuplicateKeyError


def add_student(db):
    student = {
        "student_id": input("Student ID: ").strip(),
        "first_name": input("First name: ").strip(),
        "last_name": input("Last name: ").strip(),
        "group_id": input("Group ID: ").strip(),
        "enrollment_year": int(input("Enrollment year: ").strip()),
        "status": input("Status (active/expelled/graduated): ").strip() or "active"
    }

    try:
        db.students.insert_one(student)
        print("Student added successfully.")
    except DuplicateKeyError:
        print("Error: student with this student_id already exists.")
    except Exception as e:
        print(f"Error: {e}")


def find_student(db):
    student_id = input("Enter student_id: ").strip()
    student = db.students.find_one({"student_id": student_id}, {"_id": 0})

    if student:
        print("Student found:")
        print(student)
    else:
        print("Student not found.")


def list_students(db):
    students = db.students.find({}, {"_id": 0})
    found = False

    for student in students:
        found = True
        print(student)

    if not found:
        print("No students found.")


def update_student_status(db):
    student_id = input("Enter student_id: ").strip()
    new_status = input("Enter new status (active/expelled/graduated): ").strip()

    result = db.students.update_one(
        {"student_id": student_id},
        {"$set": {"status": new_status}}
    )

    if result.matched_count:
        print("Student status updated.")
    else:
        print("Student not found.")


def delete_student(db):
    student_id = input("Enter student_id: ").strip()

    result = db.students.delete_one({"student_id": student_id})

    if result.deleted_count:
        print("Student deleted.")
    else:
        print("Student not found.")