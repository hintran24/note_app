import sqlite3

conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM note_categories')
print("Note-Categories:", cursor.fetchall())
cursor.execute('SELECT * FROM note_tags')
print("Note-Tags:", cursor.fetchall())