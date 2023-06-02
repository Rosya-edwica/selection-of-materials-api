from models import ProfessionVacancies
from api.vacancies import superjob, trudvsem
import asyncio
from itertools import chain
import time

async def find_vacancies(queryList: list[str], count: int) -> list[ProfessionVacancies]:
    tasks = [asyncio.create_task(find_task(query, count)) for query in queryList]
    vacancies: list[ProfessionVacancies] = await asyncio.gather(*tasks)
    return vacancies

async def find_task(query: str, count: int) -> ProfessionVacancies:
    print(query, time.time())
    tasks = [
        asyncio.create_task(trudvsem.find_vacancies_by_profession(query, count)),
        asyncio.create_task(superjob.find_vacancies_by_profession(query, count))
    ]
    platform_vacancies = await asyncio.gather(*tasks)
    return ProfessionVacancies(
        query=query,
        vacancies=list(chain(*platform_vacancies))
    )