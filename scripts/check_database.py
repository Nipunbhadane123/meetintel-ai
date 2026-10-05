import sqlite3
import os

DATABASE_URL = "sqlite:///meetintel.db"
db_path = DATABASE_URL.replace("sqlite:///", "")

print(f"Resolved database path: {os.path.abspath(db_path)}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Table names: {tables}")
        
        for table in ['users', 'meetings']:
            if table in tables:
                cursor.execute(f"PRAGMA table_info({table})")
                cols = [c[1] for c in cursor.fetchall()]
                print(f"Important columns in {table}: {cols}")
                
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"Row count for {table}: {count}")
                
        conn.close()
    except Exception as e:
        print(f"Error accessing database: {e}")
