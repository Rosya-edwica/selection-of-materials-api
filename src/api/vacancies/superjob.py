import os

from api.vacancies.config import get_json, update_access_token
from models import Vacancy



HEADERS = {
    "User-Agent": "",
    "Authorization": f"Bearer {os.getenv('SUPERJOB_TOKEN')}",
    "X-Api-App-id": os.getenv("SUPERJOB_SECRET")
}

async def find_vacancies_by_profession(name: str, count: int) -> list[Vacancy]:
    params = {
        "count": count,
        "keywords[0][srws]": 1, # Ищем в названии вакансии
        "keywords[0][skwc]": "particular", # Ищем точную фразу 
        "keywords[0][keys]": name, # Фраза
    }
    data = await get_json("https://api.superjob.ru/2.0/vacancies/?", params=params, headers=HEADERS)
    if not data:
        print("Пробуем снова получить токен")
        HEADERS["Authorization"] = update_access_token(HEADERS["Authorization"])
        return find_vacancies_by_profession(name)
    items = parse_vacancies(data["objects"])    
    return items[:count]

def parse_vacancies(objects: list[dict]) -> list[Vacancy]:
    items: list[Vacancy] = []
    for item in objects:
        items.append(Vacancy(
            platform="superjob",
            company=item["firm_name"],
            id=item["id"],
            url=item["link"],
            name=item["profession"],
            salary_from=item["payment_from"] if item["payment_from"] else None,
            salary_to=item["payment_to"] if item["payment_to"] else None,
            currency=item["currency"],
            skills=[]
        ))
    return items


