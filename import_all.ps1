$DB = "university_db"
$DIR = "data/seed"

Write-Host "Dropping database $DB..." -ForegroundColor Red

mongosh "mongodb://localhost:27017/$DB" --eval "db.dropDatabase()"

Write-Host "Importing data into $DB..." -ForegroundColor Yellow

mongoimport --db $DB --collection faculties --file "$DIR/faculties.jsonl"
mongoimport --db $DB --collection programs  --file "$DIR/programs.jsonl"
mongoimport --db $DB --collection groups    --file "$DIR/groups.jsonl"
mongoimport --db $DB --collection students  --file "$DIR/students.jsonl"
mongoimport --db $DB --collection teachers  --file "$DIR/teachers.jsonl"
mongoimport --db $DB --collection subjects  --file "$DIR/subjects.jsonl"
mongoimport --db $DB --collection courses   --file "$DIR/courses.jsonl"
mongoimport --db $DB --collection grades    --file "$DIR/grades.jsonl"

Write-Host "Import completed successfully!" -ForegroundColor Green
