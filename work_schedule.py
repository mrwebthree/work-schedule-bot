import calendar
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Worker rotation config
workers = ["Muhammadali", "Bunyod"]
rotation_days = 3

# State tracking (in-memory for simplicity)
start_date = datetime.strptime(os.getenv("START_DATE", "2025-03-04"), "%Y-%m-%d")
current_worker = os.getenv("START_WORKER", "Muhammadali")
schedule = {}

# Generate schedule function
def generate_schedule(start_date, start_worker):
    global schedule, current_worker
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

# Create readable schedule message
def create_schedule_message():
    message = f"📅 Work Schedule for {start_date.strftime('%B %Y')}\n\n"
    for date, worker in schedule.items():
        message += f"{date}: {worker}\n"
    return message

# Telegram command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /schedule to view shifts, or /reschedule to regenerate.")

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(create_schedule_message())

async def reschedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_date
    start_date = datetime.now()
    generate_schedule(start_date, current_worker)
    await update.message.reply_text("✅ Schedule regenerated from today!\n\n" + create_schedule_message())

async def setstart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_date, current_worker
    try:
        if len(context.args) != 2:
            raise ValueError("Invalid command format.")
        date_str, worker = context.args
        if worker not in workers:
            raise ValueError(f"Worker must be one of {workers}")

        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        current_worker = worker
        generate_schedule(start_date, current_worker)
        await update.message.reply_text(f"✅ Start date & worker updated!\n\n{create_schedule_message()}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}\nUsage: /setstart YYYY-MM-DD Worker")

async def next_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    worker = schedule.get(tomorrow_str, "(not scheduled)")
    await update.message.reply_text(f"📅 Tomorrow ({tomorrow_str}) shift: {worker}")

# Main bot function
def main():
    generate_schedule(start_date, current_worker)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schedule", schedule_command))
    app.add_handler(CommandHandler("reschedule", reschedule_command))
    app.add_handler(CommandHandler("setstart", setstart_command))
    app.add_handler(CommandHandler("next", next_command))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
