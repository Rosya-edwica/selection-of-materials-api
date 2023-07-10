from models import Vacancy
from api.vacancies.config import get_json, filter_currency


async def find_vacancies_by_profession(name: str, count: int) -> list[Vacancy]:
    params = {
        "text": name
    }
    data = await get_json(url="http://opendata.trudvsem.ru/api/v1/vacancies", params=params)
    if "vacancies" not in data["results"].keys(): return []
    items = parse_vacancies(data["results"]["vacancies"])
    return items[:count]

def parse_vacancies(objects: list[dict]) -> list[Vacancy]:
    items: list[Vacancy] = []
    for item in objects:
        vacancy = item["vacancy"]
        items.append(Vacancy(
            id=vacancy["id"],
            name=vacancy["job-name"],
            platform="trudvsem",
            company=vacancy["company"]["name"],
            salary_from=vacancy["salary_min"] if vacancy["salary_min"] else None,
            salary_to=vacancy["salary_max"] if vacancy["salary_max"] else None,
            currency=filter_currency(vacancy["currency"]),
            skills=[],
            url=vacancy["vac_url"]
        ))
    return items


