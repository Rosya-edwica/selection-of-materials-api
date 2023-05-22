from models import SkillBooks
from database import find_books_by_header, find_books_in_history

async def get_list_of_books(db, skillList: list[str], count: int, language: str = "all", free: bool = None) -> list[SkillBooks]:
    result: list[SkillBooks] = []
    for skill in skillList:
        books = await get_books(db, skill, count, language, free)
        result.append(books)
    return result


async def get_books(db, skillName: str, count: int, language: str = "all",  free: bool = None) -> SkillBooks:
    history_books, skill_exist = await find_books_in_history(db, skillName, free)
    if history_books: 
        return SkillBooks(
            skill=skillName,
            materials=history_books[:count])
    if skill_exist:
        return SkillBooks(
            skill=skillName,
            materials=[]
        )
    books = await find_books_by_header(db, skillName, count, language, free=free)
    # Пока не будем использовать поиск по описанию
    # if len(books) < count:
    #     books += await find_books_by_description(db, query, count, language, ignore = [i.id for i in books])
    return SkillBooks(
        skill=skillName,
        materials=books[:count])