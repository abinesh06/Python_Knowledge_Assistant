import sqlite3

conn = sqlite3.connect("data/pka.db")
cursor = conn.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS notes (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         text TEXT NOT NULL,
#         tags TEXT,
#         created_at TEXT NOT NULL
#     )
# """)
# conn.commit()

# print("Table created (or already existed).")

# cursor.execute(
#     "INSERT INTO notes (text, tags, created_at) VALUES (?, ?, ?)",
#     ("First SQLite note", "test", "2026-08-06")
# )
# cursor.execute(
#     "INSERT INTO notes (text, tags, created_at) VALUES (?, ?, ?)",
#     ("Second note about python", "study,python", "2026-08-06")
# )
# conn.commit()
#print("Inserted 2 rows.")

# cursor.execute("SELECT * FROM notes")
# for row in cursor.fetchall():
#     print(row)

cursor.execute("SELECT * FROM notes")
print(cursor.fetchall())


