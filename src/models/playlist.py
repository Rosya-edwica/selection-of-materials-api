from pydantic import BaseModel


class PlayList(BaseModel):
    id: str
    name: str
    link: str
    header_image: str
    

class SkillPlaylists(BaseModel):
    skill: str
    materials: list[PlayList]
