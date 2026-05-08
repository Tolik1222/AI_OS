import sys
import os

# Додаємо поточну папку в path для коректного імпорту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic import TaskManager
from database import init_db

def main():
    init_db()
    manager = TaskManager()
    
    print("=== TaskSystem Console ===")
    print("Доступні команди: add <назва>, list, exit")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input: continue
            
            parts = user_input.split(' ', 1)
            cmd = parts[0].lower()
            
            if cmd == 'exit':
                print("Вихід...")
                break
            elif cmd == 'add':
                if len(parts) > 1:
                    manager.add_task(parts[1])
                    print(f"Завдання '{parts[1]}' додано!")
                else:
                    print("Помилка: введіть назву завдання.")
            elif cmd == 'list':
                tasks = manager.get_all()
                if not tasks:
                    print("Список порожній.")
                else:
                    print("ID | Title | Status")
                    print("-" * 30)
                    for t in tasks:
                        print(f"{t[0]} | {t[1]} | {t[2]}")
            else:
                print("Невідома команда.")
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == '__main__':
    main()