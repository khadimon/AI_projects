import sqlite3
from pathlib import Path

DB = Path("papers.db")

conn = sqlite3.connect(DB)
with open("schema.sql") as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
print("Initialized the database at ", DB)