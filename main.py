import sqlite3

def show_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    print("\n--- Список користувачів у БД ---")
    for row in rows:
        print(f"ID: {row[0]} | Ім'я: {row[1]} | Email: {row[2]}")
    conn.close()

if __name__ == "__main__":
    show_users()
