# NoSQL-HW-Final

Итоговое домашнее задание (модуль 3) по учебной дисциплине **"Нереляционные базы данных"**.  
Выполнил студент магистратуры **"Инженерия данных"**: **Хорасанджян Левон**, **МИНДА251**.

## Схема базы данных

База данных `university_db` реализована в MongoDB и содержит следующие коллекции:

- `faculties` — факультеты;
- `programs` — образовательные программы;
- `groups` — учебные группы;
- `students` — студенты;
- `teachers` — преподаватели;
- `subjects` — дисциплины;
- `courses` — курсы;
- `grades` — оценки студентов.

Связи между сущностями реализованы через бизнес-идентификаторы (например, `student_id`, `course_id`, `faculty_id`). В MongoDB не используются жёсткие внешние ключи, поэтому связи реализуются логически на уровне приложения.

Основные связи:
- `students.group_id -> groups.group_id`;
- `groups.program_id -> programs.program_id`;
- `programs.faculty_id -> faculties.faculty_id`;
- `courses.subject_id -> subjects.subject_id`;
- `courses.teacher_id -> teachers.teacher_id`;
- `grades.student_id -> students.student_id`;
- `grades.course_id -> courses.course_id`.

Наиболее нагруженной коллекцией является `grades`, так как она содержит информацию о всех оценках студентов и активно растёт при добавлении новых данных.

## Структура проекта

```text
project-root/
│
├── cluster/
│   ├── configdb/
│   ├── shard1/
│   ├── shard2/
│   └── logs/
│
├── data/
│   ├── schemas/
│   └── seed/
│
├── db/
│   └── scripts/
│
├── src/
│
├── benchmark/
│   └── results/
│
├── import_all.ps1
├── requirements.txt
└── README.md
```

## Используемые технологии

- MongoDB;
- Mongo Shell (mongosh);
- PowerShell;
- Python.

## Шардинг

Для базы данных `university_db` реализован горизонтальный шардинг.

В качестве шардируемых коллекций выбраны:
- `students`;
- `grades`.

Выбор обусловлен тем, что:
- коллекция `grades` является наиболее быстрорастущей и содержит наибольшее количество записей;
- запросы к системе часто выполняются по `student_id` (например, получение оценок студента);
- коллекция `students` используется совместно с `grades`, поэтому логично использовать одинаковый ключ распределения.

В обеих коллекциях используется shard key: `{ student_id: "hashed" }`.

Использование hashed shard key позволяет:
- равномерно распределять данные между шардами;
- избежать перекоса нагрузки (hotspot);
- обеспечить более стабильную производительность при росте объёма данных.

Остальные коллекции (`faculties`, `programs`, `groups`, `teachers`, `subjects`, `courses`) не шардируются, так как:
- имеют относительно небольшой объём;
- редко изменяются;
- не создают существенной нагрузки на систему.

Все клиентские подключения и операции выполняются через `mongos`, который маршрутизирует запросы к соответствующим шардам.

## Запуск
### 1. Подготовка структуры каталогов

Перед запуском нужно создать каталоги для хранения данных и логов кластера:
```ps1
New-Item -ItemType Directory -Force .\cluster\configdb | Out-Null
New-Item -ItemType Directory -Force .\cluster\shard1   | Out-Null
New-Item -ItemType Directory -Force .\cluster\shard2   | Out-Null
New-Item -ItemType Directory -Force .\cluster\logs     | Out-Null
```

Если необходимо полностью начать с нуля, сначала остановить процессы MongoDB и очистить каталоги:
```ps1
Get-Process mongod, mongos -ErrorAction SilentlyContinue | Stop-Process -Force

Remove-Item .\cluster\configdb\* -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\cluster\shard1\*   -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\cluster\shard2\*   -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\cluster\logs\*     -Recurse -Force -ErrorAction SilentlyContinue
```

### 2. Запуск config server

В отдельном терминале:
```ps1
mongod --configsvr --replSet configReplSet --port 27019 --dbpath .\cluster\configdb --logpath .\cluster\logs\config.log --logappend
```

В другом терминале:
```ps1
mongosh --port 27019
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [
    { _id: 0, host: "localhost:27019" }
  ]
})
```

### 3. Запуск первого шарда

В отдельном терминале:
```ps1
mongod --shardsvr --replSet shard1ReplSet --port 27020 --dbpath .\cluster\shard1 --logpath .\cluster\logs\shard1.log --logappend
```

Инициализация:
```ps1
mongosh --port 27020
rs.initiate({
  _id: "shard1ReplSet",
  members: [
    { _id: 0, host: "localhost:27020" }
  ]
})
```

### 4. Запуск второго шарда

В отдельном терминале:
```ps1
mongod --shardsvr --replSet shard2ReplSet --port 27021 --dbpath .\cluster\shard2 --logpath .\cluster\logs\shard2.log --logappend
```

Инициализация:
```ps1
mongosh --port 27021
rs.initiate({
  _id: "shard2ReplSet",
  members: [
    { _id: 0, host: "localhost:27021" }
  ]
})
```

### 5. Запуск mongos

В отдельном терминале:
```ps1
mongos --configdb configReplSet/localhost:27019 --port 27018 --logpath .\cluster\logs\mongos.log --logappend
```

### 6. Добавление шардов в кластер

Подключиться к mongos:
```ps1
mongosh --port 27018
```

Выполнить:
```ps1
sh.addShard("shard1ReplSet/localhost:27020")
sh.addShard("shard2ReplSet/localhost:27021")
```

### 7. Импорт тестовых данных

Запустить PowerShell-скрипт:
```ps1
.\import_all.ps1
```

### 8. Создание supporting indexes для шардинга

Перед включением шардинга для непустых коллекций нужно создать supporting hashed indexes:
```ps1
mongosh --port 27018 .\db\scripts\pre_shard_indexes.js
```

### 9. Включение шардинга

Применить скрипт шардинга:
```ps1
mongosh --port 27018 .\db\scripts\sharding.js
```

### 10. Создание остальных индексов

После включения шардинга создать остальные индексы:
```ps1
mongosh --port 27018 .\db\scripts\indexes.js
```

## Нагрузочное тестирование

Были реализованы следующие сценарии для нагрузочного тестирования:

1. **Массовая вставка данных**
   - добавление большого количества записей в коллекцию `grades`;
   - используется `bulk_write` для повышения эффективности.
2. **Чтение данных**
   - выборка оценок по `student_id`;
   - имитация типового пользовательского запроса.
3. **Обновление данных**
   - массовое обновление статуса студентов в коллекции `students`.

Для повышения достоверности результатов тестирование выполнялось несколько раз, а результаты сохранялись в файлы с временными метками.

Все скрипты и замеры можно найти в папке [benchmark](https://github.com/lkhorasandzhian/NoSQL-HW-Final/tree/main/benchmark).

### Пример результатов

| Операция | Пропускная способность (ops/sec) |
|:---------:|:---------------------:|
| Insert (grades) | ~43 000 |
| Read (grades by student) | ~1 800 |
| Update (students) | ~15 000 |

### Анализ результатов

- Наибольшую производительность показали операции записи и обновления благодаря использованию bulk-операций.
- Операции чтения выполняются медленнее, так как включают большое количество отдельных запросов.
- Результаты нескольких прогонов показали стабильную производительность системы с незначительными отклонениями.

## Скриншоты
Все скриншоты, в т. ч. запуска через терминал, можно найти в папке [screenshots](https://github.com/lkhorasandzhian/NoSQL-HW-Final/tree/main/screenshots).
