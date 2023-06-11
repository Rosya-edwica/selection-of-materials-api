import aiohttp
import os
import dotenv


HEADERS = {
    "User-Agent": "",
    "Authorization": f"Bearer {os.getenv('SUPERJOB_TOKEN')}",
    "X-Api-App-id": os.getenv("SUPERJOB_SECRET")
}

env = dotenv.load_dotenv(".env")
if not env: exit("Ошибка! Не удалось найти файл .env!")

async def get_json(url: str, headers: dict = None, params = dict | None) -> list | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            print(resp.url)
            print(resp.content)
            if resp.status != 200: return []
            data = await resp.json()
            return data


async def update_access_token(old_token: str) -> str:
    params = {
        "refresh_token": old_token.replace("Bearer ", ""),
        "client_id": "2093",
        "client_secret": os.getenv("SUPERJOB_SECRET")
    }
    data = await get_json(url="https://api.superjob.ru/2.0/oauth2/refresh_token", params=params, headers=HEADERS)
    if not data:
        exit("Не удалось обновить токен superjob")
    token = data["access_token"]
    dotenv.set_key(".env", "SUPERJOB_TOKEN", token)
    return f"Bearer {token}"