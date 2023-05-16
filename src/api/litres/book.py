from models import Book
from database import find_books_by_header, find_books_by_description, find_books_in_history, save_query_in_history

async def get_list_of_books(query: str, count: int, language: str = "all") -> list[Book]:
    history_books = await find_books_in_history(query)
    if history_books: 
        if len(history_books) < count:
            history_books += await find_books_by_header(query, count, language, ignore = [i.id for i in history_books])
        return history_books[:count]

    books = await find_books_by_header(query, count, language)
    if len(books) == 0:
        return []
    if len(books) < count:
        books += await find_books_by_description(query, count, language, ignore = [i.id for i in books])
    return books[:count]
