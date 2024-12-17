import sqlite3  # Импортируем модуль для работы с SQLite

# Подключаемся к базе данных (файл будет создан, если его нет)
conn = sqlite3.connect('musical_tracks.sqlite')
cur = conn.cursor()

# Удаляем старые таблицы, если они уже существуют, и создаём новые
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER
);
''')

print("Таблицы созданы успешно.")  # Сообщение для проверки

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()


import csv  # Импортируем модуль для работы с CSV-файлами

# Повторно подключаемся к базе данных
conn = sqlite3.connect('musical_tracks.sqlite')
cur = conn.cursor()

# Читаем данные из файла tracks.csv и добавляем в таблицы
with open('tracks.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        artist = row['Artist']
        genre = row['Genre']
        album = row['Album']
        track = row['Track']

        # Вставляем данные в таблицы с контролем дублирования
        cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
        artist_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
        genre_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
        album_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Track (title, album_id, genre_id) VALUES (?, ?, ?)',
                    (track, album_id, genre_id))

print("Данные загружены успешно.")  # Сообщение для проверки

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

# Повторно подключаемся к базе данных
conn = sqlite3.connect('musical_tracks.sqlite')
cur = conn.cursor()

# SQL-запрос для получения нужных данных
query = '''
SELECT Track.title, Artist.name, Album.title, Genre.name 
FROM Track 
JOIN Genre ON Track.genre_id = Genre.id 
JOIN Album ON Track.album_id = Album.id 
JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Artist.name LIMIT 3
'''

print("\nРезультат запроса:")
for row in cur.execute(query):
    print(row)

# Закрываем соединение
conn.close()
