from pydantic import BaseModel

class PlayList(BaseModel):
    id: str
    name: str
    link: str
    

class PlayListDetail(BaseModel):
    id: str
    name: str
    description: str
    published_at: str
    link: str
    header_image: str
    items_count: int


class PlayListItem(BaseModel):
    id: str
    name: str
    description: str
    published_at: str
    link: str
    header_image: str