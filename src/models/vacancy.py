from pydantic import BaseModel

class Vacancy(BaseModel):
    id: str
    name: str
    platform: str
    company: str
    url: str
    salary_from: int | None
    salary_to: int | None
    currency: str
    skills: list[str]


class ProfessionVacancies(BaseModel):
    query: str
    vacancies: list[Vacancy]


class Salary(BaseModel):
    From: int
    To: int
    Currency: str
