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

def schedule_keyboard(year=None, month=None):
    from datetime import datetime

    today = datetime.today()
    if year is None or month is None:
        year, month = today.year, today.month

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("📅 To'liq jadvalni ko'rish", callback_data=f"view_schedule_{year}_{month}"))

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.row(
        telebot.types.InlineKeyboardButton("⬅️ Oldingi oy", callback_data=f"view_schedule_{prev_year}_{prev_month}"),
        telebot.types.InlineKeyboardButton("Keyingi oy ➡️", callback_data=f"view_schedule_{next_year}_{next_month}")
    )

    return keyboard
