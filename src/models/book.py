from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    description: str
    image: str | None
    url: str
    is_audio: bool
    full_price: float | None
    final_price: float | None
    currency: str | None
    min_age: int
    language: str
    rating: float
    pages: int | None
    year: int | None
