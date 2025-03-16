from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

def main_menu_keyboard():
    """Returns the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("📅 View Schedule", callback_data="view_schedule")],
        [InlineKeyboardButton("🔄 Swap Shift", callback_data="swap_shift")],
        [InlineKeyboardButton("⚙️ Set Start Date & Worker", callback_data="set_start")]
    ]
    return InlineKeyboardMarkup(keyboard)

def shift_swap_keyboard():
    """Returns a keyboard to choose extra workdays."""
    keyboard = [
        [InlineKeyboardButton("1 Day", callback_data="swap_1"), InlineKeyboardButton("2 Days", callback_data="swap_2")],
        [InlineKeyboardButton("3 Days", callback_data="swap_3")]
    ]
    return InlineKeyboardMarkup(keyboard)

def start_shift_keyboard():
    """Returns a keyboard to set a new start date and worker."""
    today = datetime.today()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    workers = ["Muhammadali", "Bunyod"]

    keyboard = []
    for date in dates:
        for worker in workers:
            keyboard.append([InlineKeyboardButton(f"{date} - {worker}", callback_data=f"set_start_{date}_{worker}")])
    
    return InlineKeyboardMarkup(keyboard)
