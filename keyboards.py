import telebot.types
from datetime import datetime, timedelta

def generate_calendar(prefix="date_"):
    today = datetime.today()
    markup = telebot.types.InlineKeyboardMarkup()

    for week in range(0, 28, 7):
        row = []
        for day_offset in range(7):
            date = today + timedelta(days=week + day_offset)
            date_str = date.strftime("%Y-%m-%d")
            row.append(telebot.types.InlineKeyboardButton(date.strftime("%d"), callback_data=f"{prefix}{date_str}"))
        markup.row(*row)

    return markup

def schedule_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("📅 To'liq jadvalni ko'rish", callback_data="view_schedule"))
    return keyboard

def modify_schedule_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("✏️ Ish jadvalini o'zgartirish", callback_data="modify_schedule"))
    return keyboard
