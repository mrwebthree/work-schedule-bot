from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    """Returns the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("📅 View Schedule", callback_data="view_schedule")],
        [InlineKeyboardButton("🔄 Reschedule", callback_data="reschedule")]
    ]
    return InlineKeyboardMarkup(keyboard)
