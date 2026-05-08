import psutil
import os
from datetime import datetime

class SysInfo:
    @staticmethod
    def get_stats():
        return {
            "cpu": psutil.cpu_percent(interval=0.1),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent
        }

    @staticmethod
    def init_logs():
        if not os.path.exists('logs'):
            os.makedirs('logs')
        with open('logs/session.log', 'a', encoding='utf-8') as f:
            f.write(f"[INFO] Монітор запущено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")