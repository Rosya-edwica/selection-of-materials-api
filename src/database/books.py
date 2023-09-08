from models import Book


async def find_books_by_header(db, query: str, count: int = 3, language: str = "all",
                               ignore: list[int] = None, free: bool = None) -> list[Book]:
    books = await find_books(db, query, language=language, ignore_list=ignore, free=free)
    if not books:
        await save_undetected_skill(db, query)
        return []
    else:
        await save_query_in_history(db, query, (book.id for book in books))  # Сохраняем всё
        return books[:count]  # Отправляем ограниченное количество


async def find_books(db, query: str, limit: int = 10, language: str = "all",
                     ignore_list: list[int] = None, free: bool = None) -> list[Book]:
    selection_query = f"""
        SELECT name, description, language, price, old_price, min_age, rating,
        year, image, url, currency, pages, is_audio, id
        FROM book 
        WHERE MATCH (name, description) AGAINST ('{query}')"""

    if ignore_list:
        selection_query += f" AND id not in ({','.join(str(i) for i in ignore_list)})"
    if language != "all":
        selection_query += f" AND language = '{language}'"
    if free is True:
        selection_query += " AND price IS NULL"
    elif free is False:
        selection_query += " AND price IS NOT NULL"
    if limit:
        selection_query += f" LIMIT {limit}"
    
    async with db.cursor() as cur:
        await cur.execute(selection_query)
        
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
            for book in await cur.fetchall()]
    return result


async def find_books_in_history(db, text: str, free: bool = None) -> tuple[list[Book], bool]:
    query = f"""
        SELECT name, description, language, price, old_price, min_age, rating,
        year, image, url, currency, pages, is_audio, book.id
        FROM book
        INNER JOIN query_to_book ON book.id = query_to_book.book_id
        WHERE LOWER(query_to_book.query) = '{text.lower().strip()}'
        """
    if free is True:
        query += " AND price IS NULL"
    elif free is False:
        query += " AND price IS NOT NULL"

    async with db.cursor() as cur:
        await cur.execute(query)
        books = [
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
            for book in await cur.fetchall()]
        
    check_skill_exist = await check_query_exists(db, text)
    if check_skill_exist:
        return books, True
    else:
        return [], False


async def check_query_exists(db, query: str) -> bool:
    async with db.cursor() as cur:
        await cur.execute(f"SELECT id FROM query_to_book WHERE LOWER(query) = '{query.lower().strip()}'")
        query_id =  await cur.fetchall()
        if query_id:
            return True
    
    return False

async def save_query_in_history(db, query: str, book_ids: list[int]):
    async with db.cursor() as cur:
        await cur.executemany(f"INSERT IGNORE INTO query_to_book(query, book_id) VALUES(%s, %s)",
                         [(query, book_id) for book_id in book_ids])
        await db.commit()

async def save_undetected_skill(db, skill: str):
    async with db.cursor() as cur:
        await cur.execute(f"INSERT IGNORE INTO query_to_book(query, book_id) VALUES('{skill}', NULL)")
        await db.commit()
