sh.enableSharding("university_db");

// Shard grades collection by student_id (hashed).
sh.shardCollection("university_db.grades", { student_id: "hashed" });

// Shard students collection by student_id (hashed).
sh.shardCollection("university_db.students", { student_id: "hashed" });