from telegram import Update
from telegram.ext import CallbackContext
from scheduler import generate_schedule, create_schedule_message, start_date, current_worker
from keyboards import main_menu_keyboard
from datetime import datetime

async def start(update: Update, context: CallbackContext):
    """Sends a welcome message with a description before showing the menu."""
    welcome_text = (
        "👋 **Welcome to the Work Schedule Bot!**\n\n"
        "This bot helps you manage and view your work schedule easily.\n"
        "🔹 Automatically generates work shifts.\n"
        "🔹 View the schedule anytime.\n"
        "🔹 Reschedule shifts with one tap.\n\n"
        "Use the buttons below to get started! ⬇️"
    )
    
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: CallbackContext):
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == "view_schedule":
        await query.edit_message_text(create_schedule_message(), reply_markup=main_menu_keyboard())

    elif query.data == "reschedule":
        global start_date
        start_date = datetime.now()
        generate_schedule(start_date, current_worker)
        await query.edit_message_text("✅ Schedule regenerated from today!\n\n" + create_schedule_message(), reply_markup=main_menu_keyboard())
