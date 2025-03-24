import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from scheduler import set_start_date, get_monthly_schedule, modify_schedule
from keyboards import schedule_keyboard, generate_calendar, modify_schedule_keyboard
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, "📅 Ish jadvalini boshlash sanasini tanlang:", reply_markup=generate_calendar())

@bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
def handle_date_selection(call):
    date_str = call.data.split("_")[1]
    user_states[call.message.chat.id] = {"date": date_str}
    
    worker_buttons = InlineKeyboardMarkup()
    worker_buttons.add(InlineKeyboardButton("👤 Muhammadali", callback_data="worker_Muhammadali"))
    worker_buttons.add(InlineKeyboardButton("👤 Bunyod", callback_data="worker_Bunyod"))

    bot.edit_message_text(f"📅 Boshlanish sanasi: {date_str}\n👤 Birinchi ishchini tanlang:", 
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=worker_buttons)

@bot.callback_query_handler(func=lambda call: call.data.startswith("worker_"))
def handle_worker_selection(call):
    worker_name = call.data.split("_")[1]
    user_data = user_states.get(call.message.chat.id, {})

    if "date" not in user_data:
        bot.send_message(call.message.chat.id, "❌ Xatolik: Iltimos, avval sanani tanlang.")
        return

    date_str = user_data["date"]
    set_start_date(date_str, worker_name)

    bot.edit_message_text(f"✅ Ish jadvali saqlandi!\n📅 Boshlanish sanasi: {date_str}\n👤 Birinchi ishchi: {worker_name}\n\n📅 To'liq jadvalni ko'rish yoki o'zgartirish uchun quyidagi tugmalardan foydalaning:",
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=schedule_keyboard())

    del user_states[call.message.chat.id]  # Clear user state

@bot.callback_query_handler(func=lambda call: call.data.startswith("view_schedule"))
def show_full_schedule(call):
    print(f"Debug: Raw call.data = {call.data}")  # ✅ Logs raw input

    # Fix: Correctly split into max 4 parts
    parts = call.data.split("_", maxsplit=3)
    print(f"Debug: Split parts = {parts}")  # ✅ Logs split parts

    if len(parts) == 1:
        from datetime import datetime
        today = datetime.today()
        year, month = today.year, today.month
    elif len(parts) == 4:
        try:
            year, month = int(parts[2]), int(parts[3])  # Ensure int conversion
        except ValueError:
            print("Debug: ValueError occurred!")  # ✅ Logs error occurrence
            bot.send_message(call.message.chat.id, "❌ Xatolik: Yil yoki oy noto‘g‘ri formatda.")
            return
    else:
        print(f"Debug: Unexpected format - {parts}")  # ✅ Logs unexpected formats
        bot.send_message(call.message.chat.id, "❌ Xatolik: Noto‘g‘ri format.")
        return

    print(f"Debug: Parsed year = {year}, month = {month}")  # ✅ Logs final parsed values

    # Fetch schedule
    schedule = get_monthly_schedule(year, month)
    # Only edit the message if the content is actually different
    if call.message.text != schedule:
        bot.edit_message_text(schedule, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=schedule_keyboard(year, month))

@bot.callback_query_handler(func=lambda call: call.data == "modify_schedule")
def modify_schedule_prompt(call):
    bot.send_message(call.message.chat.id, "📅 O'zgartirish uchun kunni tanlang:", reply_markup=generate_calendar("modify_"))

@bot.callback_query_handler(func=lambda call: call.data.startswith("modify_"))
def select_date_to_modify(call):
    date_str = call.data.split("_")[1]
    user_states[call.message.chat.id] = {"modify_date": date_str}

    worker_buttons = InlineKeyboardMarkup()
    worker_buttons.add(InlineKeyboardButton("👤 Muhammadali", callback_data="change_Muhammadali"))
    worker_buttons.add(InlineKeyboardButton("👤 Bunyod", callback_data="change_Bunyod"))

    bot.send_message(call.message.chat.id, f"📅 {date_str} sanasiga qaysi ishchini tayinlamoqchisiz?", reply_markup=worker_buttons)

@bot.callback_query_handler(func=lambda call: call.data.startswith("change_"))
def apply_schedule_change(call):
    worker_name = call.data.split("_")[1]
    user_data = user_states.get(call.message.chat.id, {})

    if "modify_date" not in user_data:
        bot.send_message(call.message.chat.id, "❌ Xatolik: Iltimos, avval sanani tanlang.")
        return

    date_str = user_data["modify_date"]
    modify_schedule(date_str, worker_name)

    bot.send_message(call.message.chat.id, f"✅ {date_str} sanasi endi {worker_name} tomonidan bajariladi!\n📅 Ish jadvalini ko'rish uchun tugmani bosing.", reply_markup=schedule_keyboard())

    del user_states[call.message.chat.id]  # Clear user state

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
