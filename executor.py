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
Ти - AI OS, оператор комп'ютера. Твоя відповідь МАЄ бути JSON-об'єктом:
1. "thoughts": "Твоє пояснення для користувача".
2. "plan": [список дій {"action": "...", ...}]

Дії: create_file, read_file, install, shell.
Якщо команди не потрібні, "plan": [].
Завжди відповідай ТІЛЬКИ JSON.
"""

def execute_plan_list(plan):
    """Виконує список команд з JSON."""
    results = []
    for cmd in plan:
        action = cmd.get("action")
        path = cmd.get("path")
        
        try:
            if action == "create_file":
                with open(path, "w", encoding="utf-8") as f:
                    f.write(cmd["content"])
                results.append(f"✅ Файл {path} створено/оновлено.")
            
            elif action == "read_file":
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        results.append(f"📄 Вміст {path}:\n{f.read()}")
                else:
                    results.append(f"❌ Файл {path} не знайдено.")
            
            elif action == "install":
                subprocess.run(["pip", "install", cmd["package"]], check=True)
                results.append(f"📦 Пакет {cmd['package']} встановлено.")
            
            elif action == "shell":
                res = subprocess.run(cmd["command"], shell=True, capture_output=True, text=True)
                results.append(f"🚀 Команда виконується... Результат: {res.stdout or res.stderr}")
        except Exception as e:
            results.append(f"❌ Помилка в дії {action}: {e}")
            
    return "\n".join(results)

def main():
    chat = client.chats.create(model=MODEL_ID, config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE")]
    ))
    
    print("🤖 AI OS 2.1 (Action-Ready) активована.")
    
    while True:
        user_input = input("\n👤 Ви: ")
        if user_input.lower() in ["exit", "вихід"]: break
        
        print("🧠 Думаю...")
        try:
            response = chat.send_message(user_input)
            
            if not response.text:
                print(" AI повернув порожню відповідь. Можливо, спрацював фільтр безпеки або стався збій зв'язку.")
                if response.candidates and response.candidates[0].finish_reason:
                    print(f"Причина зупинки: {response.candidates[0].finish_reason}")
                continue

            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            if data.get("thoughts"):
                print(f"\n🤖 AI: {data['thoughts']}")
            
            if data.get("plan"):
                print("🛠 Виконую команди...")
                feedback = execute_plan_list(data["plan"])
                print(feedback)
                
                final_response = chat.send_message(f"Результат виконання:\n{feedback}\nПрокоментуй це.")
                if final_response.text:
                    try:
                        final_data = json.loads(final_response.text.replace("```json", "").replace("```", "").strip())
                        print(f"\n🤖 AI (Підсумок): {final_data.get('thoughts')}")
                    except:
                        print(f"\n🤖 AI: {final_response.text}")

        except Exception as e:
            print(f"❌ Виникла проблема: {e}")

if __name__ == "__main__":
    main()