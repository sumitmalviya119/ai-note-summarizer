# app/database.py
import sqlite3
from datetime import datetime

def log_to_db(prompt: str, summary: str):
    print("📥 Saving to DB...")
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            summary TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO logs (prompt, summary, timestamp)
        VALUES (?, ?, ?)
    """, (prompt, summary, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()
    print("✅ Saved to DB!")

