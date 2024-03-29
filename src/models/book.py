from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    description: str
    header_image: str | None
    link: str
    is_audio: bool
    old_price: int | None
    price: int | None
    currency: str | None
    min_age: int
    language: str
    rating: float
    pages: int | None
    year: int | None


class SkillBooks(BaseModel):
    skill: str
    materials: list[Book]
    