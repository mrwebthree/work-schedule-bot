import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "START_DATE": os.getenv("START_DATE", "2025-03-04"),
        "START_WORKER": os.getenv("START_WORKER", "Muhammadali")
    }

# bot/scheduler.py
import calendar
from datetime import datetime, timedelta

workers = ["Muhammadali", "Bunyod"]
rotation_days = 3

schedule = {}


def generate_schedule(start_date, start_worker):
    global schedule
    year, month = start_date.year, start_date.month
    _, total_days = calendar.monthrange(year, month)
    schedule = {}
    current_worker = start_worker

    for day in range(1, total_days + 1):
        date = datetime(year, month, day)
        if date < start_date:
            schedule[date.strftime("%Y-%m-%d")] = "(no shift set)"
            continue

        schedule[date.strftime("%Y-%m-%d")] = current_worker

        if (date - start_date).days % rotation_days == rotation_days - 1:
            current_worker = workers[1] if current_worker == workers[0] else workers[0]


def create_schedule_message():
    message = "\ud83d\udcc5 Work Schedule\n\n"
    for date, worker in schedule.items():
        message += f"{date}: {worker}\n"
    return message


def get_worker_for_date(date):
    date_str = date.strftime("%Y-%m-%d")
    return schedule.get(date_str, "(not scheduled)")
