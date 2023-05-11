import psycopg2
import dotenv
import os

loaded = dotenv.load_dotenv(".env")
if not loaded:
    exit("Не удалось прочитать переменные окружения файла .env")


def connect():
    connection = psycopg2.connect(
        database=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT"))
    )
    return connection
