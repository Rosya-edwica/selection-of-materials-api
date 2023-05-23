import os
import dotenv
from random import randint
loaded = dotenv.load_dotenv(".env")
if not loaded:
    exit("Не удалось прочитать переменные окружения файла .env")
    

TOKEN = os.getenv("YOUTUBE_TOKEN")
domain = "https://www.youtube.com/results?"

import requests
from urllib.parse import urlencode
import json
import re

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "accept-language": "ru,en;q=0.9",
}

def get_html(query: str) -> str:
    params = {
        "search_query": query
    }
    page = requests.get(domain+urlencode(params), headers=headers)
    html = page.content.decode("utf-8")
    return html

def get_youtube_data_by_query(query: str) -> dict:
    query_filename =f"{randint(1_000_00, 5_000_00)}_timed_file.json"
    
    html = get_html(query)
    scripts = re.findall("<script.*?</script>", html)
    data = scripts[-5]
    json_data = re.sub("<script.*? =|;</script>", "", data)
    with open(query_filename, encoding="utf-8", mode="w") as file:
        json.dump(json.JSONDecoder().decode(json_data), file, ensure_ascii=True, indent=2)

    data = json.load(open(query_filename, encoding="utf-8", mode="r"))
    os.remove(query_filename)
    return data