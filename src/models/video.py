from pydantic import BaseModel

class Video(BaseModel):
    id: str
    name: str
    link: str
    

class VideoDetail(BaseModel):
    id: str
    name: str
    description: str
    link: str
    published_at: str
    tags: list[str]
    header_image: str
    views: int


class SkillVideos(BaseModel):
    skill: str
    materials: list[Video]