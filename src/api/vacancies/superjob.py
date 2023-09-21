from api.vacancies.config import get_json, update_access_token, filter_currency, HEADERS
from models import Vacancy


async def find_vacancies_by_profession(name: str, count: int, city: str = None) -> list[Vacancy]:
    params = {
        "count": count,
        "keywords[0][srws]": 1,  # Ищем в названии вакансии
        "keywords[0][skwc]": "particular",  # Ищем точную фразу
        "keywords[0][keys]": name,  # Фраза
    }
    if city:
        params["town"] = city
    data = await get_json("https://api.superjob.ru/2.0/vacancies/?", params=params, headers=HEADERS)
    if not data:
        print("Пробуем снова получить токен")
        HEADERS["Authorization"] = await update_access_token(HEADERS["Authorization"])
        vacancies = await find_vacancies_by_profession(name, count)
        return vacancies
    items = parse_vacancies(data["objects"])
    return items[:count]


def parse_vacancies(objects: list[dict]) -> list[Vacancy]:
    items: list[Vacancy] = []
    for item in objects:
        items.append(Vacancy(
            platform="superjob",
            company=item["firm_name"],
            id=str(item["id"]),
            city=item["town"]["title"],
            url=item["link"],
            name=item["profession"],
            salary_from=item["payment_from"] if item["payment_from"] else None,
            salary_to=item["payment_to"] if item["payment_to"] else None,
            currency=filter_currency(item["currency"]),
            skills=[]
        ))
    return items
