from models import ProfessionVacancies
from api.vacancies import superjob, trudvsem, geekjob
import asyncio
from itertools import chain

async def find_vacancies(queryList: list[str], count: int, platform: str = None) -> list[ProfessionVacancies]:
    tasks = [asyncio.create_task(find_task(query, count, platform)) for query in queryList]
    vacancies: list[ProfessionVacancies] = await asyncio.gather(*tasks)
    return vacancies

async def find_task(query: str, count: int, platform: str = None) -> ProfessionVacancies:
    if platform == "superjob":
        tasks = [asyncio.create_task(superjob.find_vacancies_by_profession(query, count)), ]
    elif platform == "trudvsem":
        tasks = [asyncio.create_task(trudvsem.find_vacancies_by_profession(query, count)), ]
    elif platform == "geekjob":
        tasks = [asyncio.create_task(geekjob.find_vacancies_by_profession(query, count)), ]
    else:
        tasks = [
            asyncio.create_task(trudvsem.find_vacancies_by_profession(query, count)),
            asyncio.create_task(superjob.find_vacancies_by_profession(query, count)),
            asyncio.create_task(geekjob.find_vacancies_by_profession(query, count))
        ]
    platform_vacancies = await asyncio.gather(*tasks)
    return ProfessionVacancies(
        query=query,
        vacancies=list(chain(*platform_vacancies))
    )