from fastapi import Query


QueryTextValidation = Query(
    default=..., 
    min_length=3, 
    max_length=255, 
    description="Запрос в ютубе", 
    example="PostgreSQL",
)

QueryCountValidation = Query(
    default=3, 
    gt=2, 
    le=10,
    description="Количество ожидаемых видео/плейлистов/книг",
)