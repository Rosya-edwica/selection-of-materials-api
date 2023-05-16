from models import Book, SkillBooks

async def find_books_by_header(db, query: str, count: int = 3, language: str = "all", ignore: list[int] = None) -> list[SkillBooks]:
    books = await find_books(db, query, column="title", language=language, ignoreList=ignore)
    await save_query_in_history(db, query, (book.id for book in books)) # Сохраняем всё
    return books[:count] # Отправляем ограниченное количество


async def find_books_by_description(db, query: str, count: int = 3, language: str = "all", ignore: list[int] = None) -> list[Book]:
    books = await find_books(db, query, column="description", ignoreList=ignore, language=language)
    await save_query_in_history(db, query, (book.id for book in books))
    return books[:count]

async def find_books(db, query: str, column: str, limit: int = 10, language: str = "all", ignoreList: list[int] = None) -> list[Book]:
    selection_query = f"""SELECT title, description, language, final_price, full_price, min_age, rating, year, image, url, currency, pages, is_audio, id 
        FROM book WHERE tsv_en @@ to_tsquery('english', '{query.lower()}')""" # Фиктивный лимит
    if ignoreList:
        selection_query += f" AND id not in ({','.join(str(i) for i in (ignoreList))})"
    if language != "all":
        selection_query += f" AND language = '{language}'"
    if limit:
        selection_query +=  f" LIMIT {limit}"
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
            for book in await db.fetch(selection_query)]
    return result

async def get_book_from_table(db, query: str, limit: int = None, language: str = "all", ignoreList: list[int] = None) -> list[SkillBooks]:
    query = f"""SELECT title, description, language, final_price, full_price, min_age, rating, year, image, url, currency, pages, is_audio, id 
        FROM book WHERE tsv_en @@ to_tsquery('english', '{query.lower()}') LIMIT 10"""
    if ignoreList:
        selection_query += f" AND id not in ({','.join(str(i) for i in (ignoreList))})"
    if language != "all":
        selection_query += f" AND language = '{language}'"
    if limit:
        selection_query +=  f" LIMIT {limit}"
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
            for book in await db.fetch(query)]
    return SkillBooks(
        skill=query,
        books=books[:limit]
    )

async def find_books_in_history(db, query: str) -> list[Book]:
    # query = f"""SELECT title, description, language, final_price, full_price, min_age, rating, year, image, url, currency, pages, is_audio, id
    #         FROM book WHERE id in (SELECT book_id FROM skill_to_book WHERE lower(skill) = '{query.lower().strip()}')"""
    query = f"""SELECT title, description, language, final_price, full_price, min_age, rating, year, image, url, currency, pages, is_audio, book.id
            FROM book
            INNER JOIN skill_to_book ON book.id = skill_to_book.book_id
            WHERE skill_to_book.skill = '{query.lower().strip()}'"""
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
            for book in await db.fetch(query)]
    return books


async def save_query_in_history(db, query: str, book_ids: list[int]):
    await db.executemany(f"INSERT INTO skill_to_book(skill, book_id) VALUES($1, $2) ON CONFLICT DO NOTHING", [(query, book_id) for book_id in book_ids])

def create_insert_query(values: list[str]) -> str:
    query = ",".join((f"""('{i.replace("'", '`')}')""" for i in values))
    return query