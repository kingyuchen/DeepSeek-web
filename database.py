import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('/app/history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT,
                  answer TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def save_history(question, answer):
    conn = sqlite3.connect('/app/history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (question, answer, timestamp) VALUES (?, ?, ?)",
              (question, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('/app/history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    results = c.fetchall()
    conn.close()
    return [{"id": row[0], "question": row[1], "answer": row[2], "time": row[3]} for row in results]

def delete_record(record_id):
    conn = sqlite3.connect('/app/history.db')
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()