from urllib.parse import urlencode
import aiohttp

from random import randint
import json
import os
import re


domain = "https://www.youtube.com/results?"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "accept-language": "ru,en;q=0.9",
}

async def get_html(query: str) -> str:
    params = {
        "search_query": query
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(domain+urlencode(params), headers=headers) as resp:
            html = await resp.text()
            return html.encode("utf-8")

async def get_youtube_data_by_query(query: str) -> dict:
    query_filename =f"{randint(1_000_00, 5_000_00)}_timed_file.json"
    
    html = await get_html(query)
    scripts = re.findall("<script.*?</script>", html.decode("utf-8"))
    data = scripts[-5]
    json_data = re.sub("<script.*? =|;</script>", "", data)
    with open(query_filename, encoding="utf-8", mode="w") as file:
        json.dump(json.JSONDecoder().decode(json_data), file, ensure_ascii=True, indent=2)

    data = json.load(open(query_filename, encoding="utf-8", mode="r"))
    os.remove(query_filename)
    return data
