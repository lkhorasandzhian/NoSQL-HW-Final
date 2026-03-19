from db import get_database
from student_service import (
    add_student,
    find_student,
    list_students,
    update_student_status,
    delete_student,
)
from grade_service import (
    add_grade,
    list_all_grades,
    list_student_grades,
    delete_grade,
)


def print_menu():
    print("\n=== University DB CLI ===")
    print("1. Add student")
    print("2. Find student by ID")
    print("3. List all students")
    print("4. Update student status")
    print("5. Delete student")
    print("6. Add grade")
    print("7. List all grades")
    print("8. List grades by student ID")
    print("9. Delete grade")
    print("0. Exit")
    print()


def main():
    db = get_database()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(db)
        elif choice == "2":
            find_student(db)
        elif choice == "3":
            list_students(db)
        elif choice == "4":
            update_student_status(db)
        elif choice == "5":
            delete_student(db)
        elif choice == "6":
            add_grade(db)
        elif choice == "7":
            list_all_grades(db)
        elif choice == "8":
            list_student_grades(db)
        elif choice == "9":
            delete_grade(db)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()