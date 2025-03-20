import json
from datetime import datetime, timedelta

CONFIG_FILE = "config.json"
MODIFIED_SCHEDULE = "modified_schedule.json"
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

def modify_schedule(date_str, worker_name):
    try:
        with open(MODIFIED_SCHEDULE, "r") as f:
            modified_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        modified_data = {}

    modified_data[date_str] = worker_name

    with open(MODIFIED_SCHEDULE, "w") as f:
        json.dump(modified_data, f)

def get_monthly_schedule():
    start_date, start_worker = load_start_date()
    if not start_date:
        return "❌ Ish jadvali hali o'rnatilmagan! Iltimos, /start buyrug'ini ishlating."

    try:
        with open(MODIFIED_SCHEDULE, "r") as f:
            modified_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        modified_data = {}

    today = datetime.today().date()
    first_day = today.replace(day=1)
    last_day = (first_day.replace(month=first_day.month + 1) - timedelta(days=1)).day
    
    schedule_text = "📅 Oylik ish jadvali:\n"
    for day in range(1, last_day + 1):
        date = first_day.replace(day=day)
        date_str = date.strftime("%Y-%m-%d")

        if date_str in modified_data:
            worker = modified_data[date_str]
        else:
            days_since_start = (date - start_date.date()).days
            worker_index = (days_since_start // 3) % 2
            if start_worker == "Bunyod":
                worker_index = 1 - worker_index  # Swap order if Bunyod started first
            worker = workers[worker_index]

        if date < today:
            schedule_text += f"✅ {date_str}\n"
        else:
            schedule_text += f"➡️ {date_str}: {worker}\n"

    return schedule_text
