import calendar
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Worker rotation config
workers = ["Muhammadali", "Bunyod"]
rotation_days = 3

# State tracking
start_date = datetime.strptime(os.getenv("START_DATE", "2025-03-04"), "%Y-%m-%d")
current_worker = os.getenv("START_WORKER", "Muhammadali")
schedule = {}

# Function to generate schedule
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

def create_schedule_message():
    message = f"📅 Work Schedule for {start_date.strftime('%B %Y')}\n\n"
    for date, worker in schedule.items():
        message += f"{date}: {worker}\n"
    return message

# Main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 View Schedule", callback_data="view_schedule")],
        [InlineKeyboardButton("🔄 Regenerate Schedule", callback_data="regenerate_schedule")],
        [InlineKeyboardButton("🗓 Who Works Tomorrow?", callback_data="next_worker")],
        [InlineKeyboardButton("📆 Set Start Date", callback_data="set_start_date")]
    ]
    await update.message.reply_text("👋 Welcome! Choose an option:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "view_schedule":
        await query.message.reply_text(create_schedule_message())

    elif query.data == "regenerate_schedule":
        global start_date
        start_date = datetime.now()
        generate_schedule(start_date, current_worker)
        await query.message.reply_text("✅ Schedule regenerated!\n\n" + create_schedule_message())

    elif query.data == "next_worker":
        tomorrow = datetime.now() + timedelta(days=1)
        worker = schedule.get(tomorrow.strftime("%Y-%m-%d"), "(no shift set)")
        await query.message.reply_text(f"📅 Tomorrow's shift is: {worker}")

    elif query.data == "set_start_date":
        await ask_date(update)

# Date picker menu
async def ask_date(update: Update):
    keyboard = [
        [InlineKeyboardButton("📆 Today", callback_data="date_today")],
        [InlineKeyboardButton("📅 Tomorrow", callback_data="date_tomorrow")],
        [InlineKeyboardButton("📅 Custom Date (type it)", callback_data="date_custom")],
    ]
    await update.callback_query.message.reply_text("📅 Choose start date:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handle date selection
async def date_picker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "date_today":
        context.user_data['start_date'] = datetime.now()
        await ask_worker(update)

    elif query.data == "date_tomorrow":
        context.user_data['start_date'] = datetime.now() + timedelta(days=1)
        await ask_worker(update)

    elif query.data == "date_custom":
        await query.message.reply_text("📆 Please send the date in format: YYYY-MM-DD")
        context.user_data['awaiting_date'] = True  # Waiting for text input

# Handle receiving custom date from user
async def custom_date_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'awaiting_date' in context.user_data and context.user_data['awaiting_date']:
        try:
            date = datetime.strptime(update.message.text, "%Y-%m-%d")
            context.user_data['start_date'] = date
            context.user_data.pop('awaiting_date')
            await ask_worker(update)
        except ValueError:
            await update.message.reply_text("❌ Invalid date format! Please send date as YYYY-MM-DD.")

# Worker picker menu
async def ask_worker(update: Update):
    keyboard = [
        [InlineKeyboardButton("👷 Muhammadali", callback_data="worker_Muhammadali")],
        [InlineKeyboardButton("👷 Bunyod", callback_data="worker_Bunyod")],
    ]
    await update.effective_message.reply_text("👷 Choose starting worker:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handle worker selection and regenerate schedule
async def worker_picker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    worker = query.data.split("_")[1]
    date = context.user_data.get('start_date', datetime.now())

    global start_date, current_worker
    start_date = date
    current_worker = worker

    generate_schedule(start_date, current_worker)

    await query.message.reply_text(f"✅ New schedule set from {start_date.strftime('%Y-%m-%d')} starting with {current_worker}!\n\n" + create_schedule_message())

# Main function
def main():
    generate_schedule(start_date, current_worker)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(CallbackQueryHandler(date_picker, pattern="^date_"))
    app.add_handler(CallbackQueryHandler(worker_picker, pattern="^worker_"))
    app.add_handler(CommandHandler("setstart", start))  # fallback if needed
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(None, custom_date_input))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
