from pydantic import BaseModel

class PlayList(BaseModel):
    id: str
    title: str
    url: str
    

class PlayListDetail(BaseModel):
    id: str
    title: str
    description: str
    published_at: str
    url: str
    img: str
    itemsCount: int


class PlayListItem(BaseModel):
    id: str
    title: str
    description: str
    published_at: str
    url: str
    img: str