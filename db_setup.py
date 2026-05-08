import sqlite3

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
