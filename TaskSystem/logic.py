import sqlite3
import os

class TaskManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'tasks.db')

    def add_task(self, title):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        conn.commit()
        conn.close()

    def get_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, status FROM tasks')
        tasks = cursor.fetchall()
        conn.close()
        return tasks