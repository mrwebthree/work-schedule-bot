import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from scheduler import set_start_date, get_monthly_schedule
from keyboards import schedule_keyboard, generate_calendar
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

    bot.edit_message_text(f"✅ Ish jadvali saqlandi!\n📅 Boshlanish sanasi: {date_str}\n👤 Birinchi ishchi: {worker_name}\n\n📅 To'liq jadvalni ko'rish uchun tugmani bosing:",
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=schedule_keyboard())

    del user_states[call.message.chat.id]  # Clear user state

@bot.callback_query_handler(func=lambda call: call.data == "view_schedule")
def show_full_schedule(call):
    schedule = get_monthly_schedule()
    bot.send_message(call.message.chat.id, schedule)

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
