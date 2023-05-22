from fastapi import Query


QueryTextValidation = Query(
    default=..., 
    min_length=1, 
    max_length=255, 
    description="Запрос в ютубе", 
    example="PostgreSQL",
)

QueryCountValidation = Query(
    default=3, 
    gt=0, 
    le=5,
    description="Количество ожидаемых видео/плейлистов/книг",
)

QueryLanguageValidation = Query(
    default="all",
    min_length=2,
    max_length=3,
    description="На каком языке написана книга",
    example="ru"
)

QueryBoolValidation = Query(
    default=None,
    description="True | False",
    example=True
)