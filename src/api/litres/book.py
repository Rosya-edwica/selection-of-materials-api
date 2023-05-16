from models import Book, SkillBooks
from database import find_books_by_header, find_books_by_description, find_books_in_history, save_query_in_history

async def get_list_of_books(db, skillList: list[str], count: int, language: str = "all") -> list[SkillBooks]:
    result: list[SkillBooks] = []
    for skill in skillList:
        books = await get_books(db, skill, count, language)
        result.append(books)
    return result


async def get_books(db, skillName: str, count: int, language: str = "all") -> SkillBooks:
    history_books = await find_books_in_history(db, skillName)
    if history_books: 
        return SkillBooks(
            skill=skillName,
            books=history_books[:count])

    books = await find_books_by_header(db, skillName, count, language)
    # Пока не будем использовать поиск по описанию
    # if len(books) < count:
    #     books += await find_books_by_description(db, query, count, language, ignore = [i.id for i in books])
    return SkillBooks(
        skill=skillName,
        books=books[:count])