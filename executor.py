import os
import subprocess

def run_ai_commands(commands):
    for cmd in commands:
        action = cmd.get("action")
        
        if action == "create_file":
            with open(cmd["path"], "w", encoding="utf-8") as f:
                f.write(cmd["content"])
            print(f"✅ Файл створено: {cmd['path']}")
            
        elif action == "install":
            print(f"⏳ Встановлення: {cmd['package']}...")
            subprocess.run(["pip", "install", cmd["package"]])
            
        elif action == "shell":
            print(f"🚀 Запуск команди: {cmd['command']}")
            subprocess.run(cmd["command"], shell=True)

example_plan = [
    {
        "action": "create_file", 
        "path": "db_setup.py", 
        "content": """import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    
    users = [('Олексій', 'alex@mail.com'), ('Марія', 'maria@dev.ua'), ('AI_Agent', 'agent@os.ai')]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users)
    
    conn.commit()
    conn.close()
    print("✅ База даних створена, таблиця 'users' заповнена!")

if __name__ == "__main__":
    init_db()
"""
    },
    {
        "action": "create_file", 
        "path": "main.py", 
        "content": """import sqlite3

def show_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    print("\\n--- Список користувачів у БД ---")
    for row in rows:
        print(f"ID: {row[0]} | Ім'я: {row[1]} | Email: {row[2]}")
    conn.close()

if __name__ == "__main__":
    show_users()
"""
    },
    {
        "action": "shell", 
        "command": "python db_setup.py"
    },
    {
        "action": "shell", 
        "command": "python main.py"
    }
]

if __name__ == "__main__":
    # Для першого тесту просто запустимо приклад
    run_ai_commands(example_plan)