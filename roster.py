import json
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('roster.sqlite')
cur = conn.cursor()

# Удаляем старые таблицы, если они существуют
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

# Загружаем JSON-файл
fname = 'roster_data.json'
with open(fname) as f:
    data = json.load(f)

# Заполняем таблицы данными из JSON
for entry in data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    # Добавляем User
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    # Добавляем Course
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]

    # Добавляем Member с role
    cur.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)',
                (user_id, course_id, role))

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Данные загружены успешно.")
