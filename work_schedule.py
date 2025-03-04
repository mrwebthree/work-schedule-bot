import calendar
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

START_DATE = os.getenv("START_DATE", "2025-03-04")
START_WORKER = os.getenv("START_WORKER", "Muhammadali")

workers = ["Muhammadali", "Bunyod"]
rotation_days = 3

# Convert start date to datetime object
start_date = datetime.strptime(START_DATE, "%Y-%m-%d")

# Make sure start worker is valid
if START_WORKER not in workers:
    raise ValueError(f"START_WORKER must be one of {workers}")

# Generate schedule for the whole month
year, month = start_date.year, start_date.month
_, total_days = calendar.monthrange(year, month)

schedule = {}
current_worker = START_WORKER

# Logic to fill the month from the given start date
for day in range(1, total_days + 1):
    date = datetime(year, month, day)
    if date < start_date:
        schedule[date.strftime("%Y-%m-%d")] = "(no shift set)"  # Past days if needed
        continue

    schedule[date.strftime("%Y-%m-%d")] = current_worker

    # Swap worker after every 3 days
    if (date - start_date).days % rotation_days == rotation_days - 1:
        current_worker = workers[1] if current_worker == workers[0] else workers[0]

# Format message
def create_schedule_message():
    message = f"📅 Updated Work Schedule for {start_date.strftime('%B %Y')}\n\n"
    for date, worker in schedule.items():
        message += f"{date}: {worker}\n"
    return message

# Send schedule to Telegram
def send_schedule_to_telegram():
    message = create_schedule_message()

    # Save to file too (for your local record)
    with open("work_schedule.txt", "w", encoding="utf-8") as file:
        file.write(message)

    # Send to Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("✅ Schedule sent to Telegram!")
    else:
        print(f"❌ Failed to send schedule. Response: {response.text}")

# Main execution
if __name__ == "__main__":
    send_schedule_to_telegram()
