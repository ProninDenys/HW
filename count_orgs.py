import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Создание таблицы
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Открытие файла
fname = input('Enter file name: ')  # Введите "mbox.txt"
if len(fname) < 1:
    fname = 'mbox.txt'
fh = open(fname)

# Обработка строк файла
for line in fh:
    if not line.startswith('From: '):  # Обработка строк, содержащих "From:"
        continue
    pieces = line.split()
    email = pieces[1]
    org = email.split('@')[1]  # Извлекаем домен (org)

    # Обновление базы данных
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))

# Сохранение и закрытие
conn.commit()
cur.close()
print('Done')
