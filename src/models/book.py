from pydantic import BaseModel

class Book(BaseModel):
    id: int
    name: str
    description: str
    header_image: str | None
    link: str
    is_audio: bool
    old_price: float | None
    price: float | None
    currency: str | None
    min_age: int
    language: str
    rating: float
    pages: int | None
    year: int | None
