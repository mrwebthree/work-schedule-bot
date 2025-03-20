import telebot.types
from datetime import datetime, timedelta

def generate_calendar():
    today = datetime.today()
    markup = telebot.types.InlineKeyboardMarkup()

    for week in range(0, 28, 7):  # Generate 4 weeks
        row = []
        for day_offset in range(7):
            date = today + timedelta(days=week + day_offset)
            date_str = date.strftime("%Y-%m-%d")
            row.append(telebot.types.InlineKeyboardButton(date.strftime("%d"), callback_data=f"date_{date_str}"))
        markup.row(*row)

    return markup

def schedule_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("📅 To'liq jadvalni ko'rish", callback_data="view_schedule")
    keyboard.add(button)
    return keyboard
