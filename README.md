# NoSQL-HW-Final

Итоговое домашнее задание (модуль 3) по учебной дисциплине **"Нереляционные базы данных"**.  
Выполнил студент магистратуры **"Инженерия данных"**: **Хорасанджян Левон**, **МИНДА251**.

## Описание проекта

В рамках работы реализована база данных университета на MongoDB со следующими сущностями:
- факультеты;
- образовательные программы;
- учебные группы;
- студенты;
- преподаватели;
- дисциплины;
- курсы;
- оценки.

Для проекта реализованы:
- проектирование схемы данных;
- импорт тестовых данных;
- система индексов;
- горизонтальное масштабирование с помощью шардинга;
- подготовка к созданию клиентского интерфейса на Python;
- база для последующего нагрузочного тестирования.

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
├── import_all.ps1
└── README.md
```

## Используемые технологии

- MongoDB;
- Mongo Shell (mongosh);
- PowerShell;
- Python.

## Шардинг

Для базы данных university_db реализован шардинг двух наиболее важных коллекций:
- students;
- grades.

В обеих коллекциях в качестве shard key используется: `{ student_id: "hashed" }`.  
Такой подход позволяет равномернее распределять данные между шардами и снижать риск перекоса нагрузки.

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

## Скриншоты
Все скриншоты, в т. ч. запуска через терминал, можно найти в папке `screenshots`.
