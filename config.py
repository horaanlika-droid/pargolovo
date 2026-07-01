import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]

# Каналы для публикации достижений
CHANNELS = ["chat_goddes"]

# Лимиты
MAX_SCENE_HISTORY = 50
DEFAULT_ROLLS = 0
