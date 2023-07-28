from models import SkillBooks
from database import find_books_by_header, find_books_in_history


async def get_list_of_books(db, skill_list: list[str], count: int, language: str = "all", free: bool = None) \
        -> list[SkillBooks]:
    result: list[SkillBooks] = []
    for skill in skill_list:
        books = await get_books(db, skill, count, language, free)
        result.append(books)
    return result


async def get_books(db, text: str, count: int, language: str = "all",  free: bool = None) -> SkillBooks:
    history_books, skill_exist = await find_books_in_history(db, text, free)
    if history_books: 
        return SkillBooks(
            skill=text,
            materials=history_books[:count])
    if skill_exist:
        return SkillBooks(
            skill=text,
            materials=[]
        )
    books = await find_books_by_header(db, text, count, language, free=free)
    return SkillBooks(
        skill=text,
        materials=books[:count])
