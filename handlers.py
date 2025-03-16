from telegram import Update
from telegram.ext import CallbackContext
from scheduler import generate_schedule, create_schedule_message, swap_shift
from keyboards import main_menu_keyboard, shift_swap_keyboard
from datetime import datetime

async def start(update: Update, context: CallbackContext):
    """Sends a welcome message with the main menu."""
    welcome_text = (
        "👋 **Welcome to the Work Schedule Bot!**\n\n"
        "This bot helps you manage and view your work schedule easily.\n"
        "🔹 Automatically generates work shifts.\n"
        "🔹 View the schedule anytime.\n"
        "🔹 Swap shifts with your coworker dynamically.\n\n"
        "Use the buttons below to get started! ⬇️"
    )
    
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: CallbackContext):
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == "view_schedule":
        await query.edit_message_text(create_schedule_message(), reply_markup=main_menu_keyboard())

    elif query.data == "swap_shift":
        await query.edit_message_text("🔄 Select shift to swap:", reply_markup=shift_swap_keyboard())

    elif query.data.startswith("confirm_swap_"):
        shift_info = query.data.split("_")[2]  # Example: "2025-03-20"
        success = swap_shift(shift_info)

        if success:
            await query.edit_message_text(f"✅ Shift on {shift_info} swapped successfully!\n\n" + create_schedule_message(), reply_markup=main_menu_keyboard())
        else:
            await query.edit_message_text("❌ Shift swap failed. Check if it's a valid date.", reply_markup=main_menu_keyboard())
