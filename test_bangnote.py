import sqlite3

conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM notes')
print("Notes:", cursor.fetchall())
conn.close()