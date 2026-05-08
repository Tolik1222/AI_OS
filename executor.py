import os
import subprocess
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-flash-latest"

SYSTEM_PROMPT = """
Ти - AI OS Project Architect. Твоя відповідь МАЄ бути ТІЛЬКИ JSON-об'єктом.
Формат відповіді:
{
  "thoughts": "пояснення твоїх дій",
  "plan": [
    {"action": "create_file", "path": "шлях", "content": "..."},
    {"action": "shell", "command": "..."},
    {"action": "read_file", "path": "..."}
  ]
}
Дії: create_file (автоматично створює папки), shell, read_file.
Завжди розбивай великі завдання на логічні файли.
"""

def execute_plan_list(plan):
    results = []
    if not isinstance(plan, list):
        return " Помилка: 'plan' має бути списком."

    for cmd in plan:
        if not isinstance(cmd, dict): continue
        
        action = cmd.get("action")
        path = cmd.get("path")
        
        try:
            if action == "create_file" and path:
                directory = os.path.dirname(path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    results.append(f" Створено папку: {directory}")
                
                content = cmd.get("content", "")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                results.append(f" Файл {path} створено.")
            
            elif action == "read_file" and path:
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        results.append(f" Вміст {path}:\n{f.read()}")
                else:
                    results.append(f" Файл {path} не знайдено.")
            
            elif action == "shell":
                cmd_text = cmd.get("command")
                res = subprocess.run(cmd_text, shell=True, capture_output=True, text=True)
                results.append(f" Команда: {cmd_text}\nВивід: {res.stdout or res.stderr}")
        
        except Exception as e:
            results.append(f" Помилка в дії {action}: {e}")
            
    return "\n".join(results)

def main():
    chat = client.chats.create(model=MODEL_ID, config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE")]
    ))
    
    print(" AI OS активована.")
    
    while True:
        user_input = input("\n Ви: ")
        if user_input.lower() in ["exit", "вихід"]: break
        
        structure = get_folder_structure()
        full_query = f"Поточна структура проєкту:\n{structure}\n\nЗапит: {user_input}"
        
        print(" Думаю...")
        try:
            response = chat.send_message(full_query)
            
            if not response.text:
                print(" Порожня відповідь від ШІ.")
                continue

            try:
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
            except Exception as parse_error:
                print(f" Помилка парсингу відповіді: {parse_error}")
                print(f"Текст відповіді: {response.text}")
                continue
            
            if isinstance(data, dict) and data.get("thoughts"):
                print(f"\n AI: {data['thoughts']}")
            
            plan = data.get("plan") if isinstance(data, dict) else []
            if plan:
                print("🛠 Виконую команди...")
                feedback = execute_plan_list(plan)
                print(feedback)
                
                chat.send_message(f"Результат виконання: {feedback}. Прокоментуй успіх.")

        except Exception as e:
            print(f" Критична помилка: {e}")

def get_folder_structure(root_dir="."):
    exclude = {'.git', '.env', '__pycache__', 'venv'}
    tree = []
    try:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in exclude]
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree.append(f"{indent}{os.path.basename(root) or root}/")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if f not in exclude:
                    tree.append(f"{sub_indent}{f}")
    except: return "Не вдалося зчитати структуру."
    return "\n".join(tree)

if __name__ == "__main__":
    main()