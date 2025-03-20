import json
from datetime import datetime, timedelta

CONFIG_FILE = "config.json"
workers = ["Muhammadali", "Bunyod"]

def load_start_date():
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return datetime.strptime(data["start_date"], "%Y-%m-%d"), data["start_worker"]
    except (FileNotFoundError, KeyError):
        return None, None  # No start date set yet

def set_start_date(date_str, worker_name):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"start_date": date_str, "start_worker": worker_name}, f)

def get_monthly_schedule():
    start_date, start_worker = load_start_date()
    if not start_date:
        return "❌ Ish jadvali hali o'rnatilmagan! Iltimos, /start buyrug'ini ishlating."

    today = datetime.today().date()
    first_day = today.replace(day=1)
    last_day = (first_day.replace(month=first_day.month + 1) - timedelta(days=1)).day
    
    schedule_text = "📅 Oylik ish jadvali:\n"
    for day in range(1, last_day + 1):
        date = first_day.replace(day=day)
        days_since_start = (date - start_date.date()).days
        worker_index = (days_since_start // 3) % 2

        if start_worker == "Bunyod":
            worker_index = 1 - worker_index  # Swap order if Bunyod started first
        
        if date < today:
            schedule_text += f"✅ {date.strftime('%Y-%m-%d')}\n"
        else:
            schedule_text += f"➡️ {date.strftime('%Y-%m-%d')}: {workers[worker_index]}\n"

    return schedule_text
