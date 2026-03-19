$DB = "university_db"
$DIR = "data/seed"

Write-Host "Dropping database $DB..." -ForegroundColor Red

mongosh "mongodb://localhost:27018/$DB" --eval "db.dropDatabase()"

Write-Host "Importing data into $DB..." -ForegroundColor Yellow

mongoimport --uri "mongodb://localhost:27018/$DB" --collection faculties --file "$DIR/faculties.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection programs  --file "$DIR/programs.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection groups    --file "$DIR/groups.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection students  --file "$DIR/students.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection teachers  --file "$DIR/teachers.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection subjects  --file "$DIR/subjects.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection courses   --file "$DIR/courses.jsonl"
mongoimport --uri "mongodb://localhost:27018/$DB" --collection grades    --file "$DIR/grades.jsonl"

Write-Host "Import completed successfully!" -ForegroundColor Green
