from models import ProfessionVacancies
from api.vacancies import superjob, trudvsem, geekjob
import asyncio
from itertools import chain


async def find_vacancies(query_list: list[str], count: int, platform: str = None, city: str = None) \
        -> list[ProfessionVacancies]:
    tasks = [asyncio.create_task(find_task(query, count, platform, city)) for query in query_list]
    vacancies: list[ProfessionVacancies] = await asyncio.gather(*tasks)
    return vacancies


async def find_task(query: str, count: int, platform: str = None, city: str = None) -> ProfessionVacancies:
    match platform:
        case "superjob": tasks = [asyncio.create_task(superjob.find_vacancies_by_profession(query, count, city)), ]
        case "trudvsem": tasks = [asyncio.create_task(trudvsem.find_vacancies_by_profession(query, count)), ]
        case "geekjob": tasks = [asyncio.create_task(geekjob.find_vacancies_by_profession(query, count)), ]
        case _:
            tasks = [
                asyncio.create_task(trudvsem.find_vacancies_by_profession(query, count)),
                asyncio.create_task(superjob.find_vacancies_by_profession(query, count, city)),
                asyncio.create_task(geekjob.find_vacancies_by_profession(query, count))
            ]
    platform_vacancies = await asyncio.gather(*tasks)
    return ProfessionVacancies(
        query=query,
        vacancies=list(chain(*platform_vacancies))
    )
