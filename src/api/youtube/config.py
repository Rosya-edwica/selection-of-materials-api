import os
import dotenv

loaded = dotenv.load_dotenv(".env")
if not loaded:
    exit("Не удалось прочитать переменные окружения файла .env")
    

TOKEN = os.getenv("YOUTUBE_TOKEN")