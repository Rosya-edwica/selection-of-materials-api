from pydantic import BaseModel

class Video(BaseModel):
    id: str
    title: str
    url: str
    

class VideoDetail(BaseModel):
    id: str
    title: str
    description: str
    url: str
    published_at: str
    tags: list[str]
    img: str
    views: int