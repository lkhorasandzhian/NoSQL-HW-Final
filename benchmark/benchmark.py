import json
import random
import string
import time
import os
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient, InsertOne, UpdateOne

MONGO_URI = "mongodb://localhost:27018/"
DB_NAME = "university_db"


def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]


def random_grade_id(prefix="BG"):
    suffix = "".join(random.choices(string.digits, k=8))
    return f"{prefix}{suffix}"


def generate_grade_doc(student_id: str, index: int):
    course_ids = ["COURSE2025-M2-DB", "COURSE2025-M1-ALG"]
    grade_types = ["exam", "hw", "lab", "project"]

    return {
        "grade_id": random_grade_id(),
        "student_id": student_id,
        "course_id": random.choice(course_ids),
        "grade_type": random.choice(grade_types),
        "grade_value": random.randint(4, 10),
        "date": datetime.now(timezone.utc) - timedelta(days=index % 365),
        "comment": f"Benchmark grade #{index}"
    }


def benchmark_bulk_insert_grades(db, total_docs=10000, batch_size=1000):
    collection = db.grades
    student_ids = [f"S{20250000 + i}" for i in range(1, 101)]

    start = time.perf_counter()

    inserted = 0
    for batch_start in range(0, total_docs, batch_size):
        operations = []
        for i in range(batch_start, min(batch_start + batch_size, total_docs)):
            student_id = random.choice(student_ids)
            operations.append(InsertOne(generate_grade_doc(student_id, i)))
        collection.bulk_write(operations, ordered=False)
        inserted += len(operations)

    elapsed = time.perf_counter() - start
    return {
        "test_name": "bulk_insert_grades",
        "operations": inserted,
        "elapsed_seconds": round(elapsed, 4),
        "throughput_ops_sec": round(inserted / elapsed, 2) if elapsed > 0 else 0
    }


def benchmark_read_grades_by_student(db, total_queries=5000):
    collection = db.grades
    student_ids = [doc["student_id"] for doc in db.students.find({}, {"_id": 0, "student_id": 1})]

    if not student_ids:
        raise RuntimeError("No students found in database for read benchmark.")

    start = time.perf_counter()

    for _ in range(total_queries):
        sid = random.choice(student_ids)
        list(collection.find({"student_id": sid}, {"_id": 0}))

    elapsed = time.perf_counter() - start
    return {
        "test_name": "read_grades_by_student",
        "operations": total_queries,
        "elapsed_seconds": round(elapsed, 4),
        "throughput_ops_sec": round(total_queries / elapsed, 2) if elapsed > 0 else 0
    }


def benchmark_update_student_status(db, total_updates=3000, batch_size=500):
    collection = db.students
    student_ids = [doc["student_id"] for doc in db.students.find({}, {"_id": 0, "student_id": 1})]

    if not student_ids:
        raise RuntimeError("No students found in database for update benchmark.")

    statuses = ["active", "graduated", "expelled"]
    start = time.perf_counter()

    updated = 0
    for batch_start in range(0, total_updates, batch_size):
        operations = []
        for _ in range(min(batch_size, total_updates - batch_start)):
            sid = random.choice(student_ids)
            new_status = random.choice(statuses)
            operations.append(
                UpdateOne(
                    {"student_id": sid},
                    {"$set": {"status": new_status}}
                )
            )
        result = collection.bulk_write(operations, ordered=False)
        updated += result.modified_count + result.matched_count

    elapsed = time.perf_counter() - start
    return {
        "test_name": "update_student_status",
        "operations": total_updates,
        "elapsed_seconds": round(elapsed, 4),
        "throughput_ops_sec": round(total_updates / elapsed, 2) if elapsed > 0 else 0
    }


def main():
    db = get_db()

    print("Starting benchmark...")

    results = []
    results.append(benchmark_bulk_insert_grades(db, total_docs=10000, batch_size=1000))
    results.append(benchmark_read_grades_by_student(db, total_queries=5000))
    results.append(benchmark_update_student_status(db, total_updates=3000, batch_size=500))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results_dir = "benchmark/results"
    os.makedirs(results_dir, exist_ok=True)

    filename = f"{results_dir}/benchmark_{timestamp}.json"

    results_metadata = {
        "timestamp": timestamp,
        "total_tests": len(results),
        "results": results
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results_metadata, f, ensure_ascii=False, indent=2)

    print("Benchmark completed.")
    print(f"Results saved to: {filename}")
    print(json.dumps(results_metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()