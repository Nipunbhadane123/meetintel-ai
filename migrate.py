import sqlite3
import os

db_path = "data/meetintel.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE meetings ADD COLUMN file_hash TEXT")
        conn.commit()
        print("Migration successful: file_hash added.")
    except sqlite3.OperationalError as e:
        print(f"Migration error (already exists?): {e}")
    conn.close()
