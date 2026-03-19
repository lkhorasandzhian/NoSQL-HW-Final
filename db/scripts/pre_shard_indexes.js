use("university_db");

db.students.createIndex({ student_id: "hashed" });
db.grades.createIndex({ student_id: "hashed" });