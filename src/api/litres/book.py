from models import Book
from database import find_books_by_header, find_books_by_description, find_books_in_history, save_query_in_history

async def get_list_of_books(db, query: str, count: int, language: str = "all") -> list[Book]:
    history_books = await find_books_in_history(db, query)
    if history_books: 
        return history_books[:count]

    books = await find_books_by_header(db, query, count, language)
    # Пока не будем использовать поиск по описанию
    # if len(books) < count:
    #     books += await find_books_by_description(db, query, count, language, ignore = [i.id for i in books])
    return books[:count]
