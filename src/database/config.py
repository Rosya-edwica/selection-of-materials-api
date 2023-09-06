import dotenv
import os
import asyncpg
import aiomysql

loaded = dotenv.load_dotenv(".env")
if not loaded:
    exit("Не удалось прочитать переменные окружения файла .env")


# async def connect():
#     connection = await asyncpg.connect(
#         database=os.getenv("POSTGRES_DATABASE"),
#         user=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=int(os.getenv("POSTGRES_PORT"))
#     )
#     return connection

async def connect(loop):
    connection = await aiomysql.connect(
        db=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        loop=loop)
    return connection