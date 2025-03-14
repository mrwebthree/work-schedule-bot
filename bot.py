from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from env_loader import TELEGRAM_BOT_TOKEN
from handlers import start, button_handler

def main():
    """Starts the bot."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
