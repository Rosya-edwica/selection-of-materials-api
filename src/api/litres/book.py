from models import Book
from database import find_books_by_header, find_books_by_description

async def get_list_of_books(query: str, count: int, language: str = "all") -> list[Book]:
    books = await find_books_by_header(query, count, language)
    if len(books) < count:
        books += await find_books_by_description(query, count, language, ignore = [i.id for i in books])
    return books[:count]
