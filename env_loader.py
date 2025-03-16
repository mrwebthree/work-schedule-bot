import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
START_DATE = os.getenv("START_DATE", "2025-03-01")
START_WORKER = os.getenv("START_WORKER", "Bunyod")
