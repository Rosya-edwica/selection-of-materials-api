import re
import logging

import asyncio
from bs4 import BeautifulSoup
from api.vacancies.config import get_soup, get_json, filter_currency

from models import Vacancy, Salary


VACANCY_URL = "https://geekjob.ru/vacancy/"
SEARCH_URL = "https://geekjob.ru/json/find/vacancy?"


async def find_vacancies_by_profession(name: str, count: int) -> list[Vacancy]:
    params = {
        "qs": name
    }
    data = await get_json(SEARCH_URL, params=params)
    if not data["data"]:
        return []
    vacancy_ids = [item["id"] for item in data["data"] if not item["log"]["archived"]][:count]
    tasks = [asyncio.create_task(parse_vacancy(vacancy_id)) for vacancy_id in vacancy_ids]
    vacancies = [item for item in await asyncio.gather(*tasks) if item is not None]
    return vacancies


async def parse_vacancy(vacancy_id: str) -> Vacancy:
    try:
        soup = await get_soup(VACANCY_URL + vacancy_id)
        salary = parse_salary(soup)
        vacancy = Vacancy(
            id=vacancy_id,
            name=soup.find("h1").text,
            platform="geekjob",
            city=get_city(soup),
            company=soup.find("h5", class_="company-name").find("a").text,
            url=VACANCY_URL+vacancy_id,
            salary_from=salary.From,
            salary_to=salary.To,
            currency=salary.Currency,
            skills=[]  # Навыки в описании вакансии
        )
        return vacancy
    except BaseException as err:
        logging.info(f"Вакансия в архиве:{vacancy_id}")  # Вакансия недоступна, т.к. находится в архиве

def parse_salary(soup: BeautifulSoup) -> Salary:
    text = soup.find("span", class_="salary").text
    salary_ints = [int(item.replace(" ", "")) for item in re.findall(r"\d+ 000", text)]  # Выбираем "100 000 | 40 000 | 10 000"
    if len(salary_ints) == 0:
        return Salary(
            From=0,
            To=0,
            Currency="RUR"
        )
    elif len(salary_ints) == 2:
        return Salary(
            From=salary_ints[0],
            To=salary_ints[1],
            Currency=filter_currency(text[-1])  # Последний символ строки "От 100 000 до 120 000 ₽"
        )
    else:
        return Salary(
            From=salary_ints[0],
            To=salary_ints[0],
            Currency=filter_currency(text[-1])
        )


def get_city(soup: BeautifulSoup) -> str:
    city = soup.find("div", class_="location")
    if city:
        return city.text.split(",")[0]
    return ""
