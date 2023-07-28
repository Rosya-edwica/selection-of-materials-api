from pydantic import BaseModel


class Video(BaseModel):
    id: str
    name: str
    link: str
    header_image: str
    

class SkillVideos(BaseModel):
    skill: str
    materials: list[Video]
