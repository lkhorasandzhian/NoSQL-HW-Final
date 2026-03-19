use("university_db");

// Faculties.
db.faculties.createIndex({ faculty_id: 1 }, { unique: true });

// Programs.
db.programs.createIndex({ program_id: 1 }, { unique: true });
db.programs.createIndex({ faculty_id: 1 });

// Groups.
db.groups.createIndex({ group_id: 1 }, { unique: true });
db.groups.createIndex({ program_id: 1 });

// Students.
db.students.createIndex({ student_id: 1 }, { unique: true });
db.students.createIndex({ group_id: 1 });

// Teachers.
db.teachers.createIndex({ teacher_id: 1 }, { unique: true });
db.teachers.createIndex({ faculty_id: 1 });

// Subjects.
db.subjects.createIndex({ subject_id: 1 }, { unique: true });
db.subjects.createIndex({ faculty_id: 1 });

// Courses.
db.courses.createIndex({ course_id: 1 }, { unique: true });
db.courses.createIndex({ subject_id: 1 });
db.courses.createIndex({ teacher_id: 1 });
db.courses.createIndex({ semester: 1 });
db.courses.createIndex({ groups: 1 });

// Grades.
db.grades.createIndex({ grade_id: 1 }, { unique: true });
db.grades.createIndex({ student_id: 1 });
db.grades.createIndex({ course_id: 1 });
db.grades.createIndex({ grade_type: 1 });
db.grades.createIndex({ student_id: 1, course_id: 1 });
db.grades.createIndex({ course_id: 1, grade_type: 1 });