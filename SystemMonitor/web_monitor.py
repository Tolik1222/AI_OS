from flask import Flask, render_template
from monitor import SysInfo

app = Flask(__name__)

# Автоматична ініціалізація логів
SysInfo.init_logs()

@app.route('/')
def index():
    stats = SysInfo.get_stats()
    return render_template('monitor.html', stats=stats)

if __name__ == '__main__':
    print("Сервер запущено на http://127.0.0.1:5000")
    app.run(debug=True, port=5000)