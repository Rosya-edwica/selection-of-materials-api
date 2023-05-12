from database import connect
from models import Book


def find_books_by_header(query: str, count: int = 3, language: str = "all") -> list[Book]:
    books = find_books(query, column="title", limit=count, language=language)
    return books


def find_books_by_description(query: str, count: int = 3, language: str = "all", ignore: list[int] = None) -> list[Book]:
    books = find_books(query, column="description", limit=count, ignoreList=ignore, language=language)
    return books


def find_books(query: str, column: str, limit: int = None, language: str = "all", ignoreList: list[int] = None) -> list[Book]:
    connection = connect()
    selection_query = f"""SELECT title, description, language, final_price, full_price, min_age, rating, year, image, url, currency, pages, is_audio, id 
        FROM book WHERE lower({column}) LIKE '% {query.lower().strip()}%'"""
    if ignoreList:
        selection_query += f" AND id not in ({','.join(str(i) for i in (ignoreList))})"
    if language != "all":
        selection_query += f" AND language = '{language}'"
    if limit:
        selection_query +=  f" LIMIT {limit}"

    cursor = connection.cursor()
    cursor.execute(selection_query)
    result = [
        Book(
            name=book[0],
            description=book[1],
            language=book[2],
            price=book[3],
            old_price=book[4],
            min_age=book[5],
            rating=book[6],
            year=book[7],
            header_image=book[8],
            link=book[9],
            currency=book[10],
            pages=book[11],
            is_audio=book[12],
            id=book[13]
        ) 
            for book in cursor.fetchall()]
    return result