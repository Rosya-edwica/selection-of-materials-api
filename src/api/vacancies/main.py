from models import ProfessionVacancies
from api.vacancies import superjob, trudvsem

async def find_vacancies(queryList: list[str], count: int) -> list[ProfessionVacancies]:
    vacancies: list[ProfessionVacancies] = []
    for query in queryList:
        trudvsem_vacancies = await trudvsem.find_vacancies_by_profession(query, count)
        superjob_vacancies = await superjob.find_vacancies_by_profession(query, count)
        vacancies.append(ProfessionVacancies(
            query=query,
            vacancies=superjob_vacancies+trudvsem_vacancies
        ))
    return vacancies