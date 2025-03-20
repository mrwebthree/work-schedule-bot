import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_env_variable(key):
    return os.getenv(key)
