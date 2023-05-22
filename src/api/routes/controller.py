from fastapi import APIRouter
from typing import List

from api.validation import *
from models import *
import database
from api import youtube, litres


router = APIRouter()

@router.get("/")
async def home():
    return {
        "success": "true",
        "message": "Документация проекта: http://api.edwica.ru/docs"
        }

@router.get("/videos", response_model=list[SkillVideos], description="Подбор видео под конкретный навык")
async def search_list_of_videos(text: List[str] = QueryTextValidation, count: int = QueryCountValidation) -> list[SkillVideos]:
    videos = youtube.get_list_of_video(text, count)
    return videos

@router.get("/videos/{id}", response_model=VideoDetail, description="Подробная информация о видео")
async def search_video(id: str) -> VideoDetail:
    video = youtube.get_video(id)
    if not video: return NOT_FOUND
    return video

@router.get("/playlists", response_model=list[SkillPlaylists], description="Подбор плейлистов под конкретный навык")
async def search_list_of_playlists(text: List[str] = QueryTextValidation, count: int = QueryCountValidation) -> list[SkillPlaylists]:
    playlists = youtube.get_list_of_playlist(text, count)
    return playlists

@router.get("/playlists/{id}", response_model=PlayListDetail, description="Подробная информация о плейлисте")
async def search_playlist(id: str) -> PlayListDetail:
    playlist = youtube.get_playlist(id) 
    if not playlist: return NOT_FOUND
    return playlist


@router.get("/playlists/{id}/items", response_model=list[PlayListItem], description="Список видео, принадлежащих плейлисту")
async def search_playlist_items(id: str) -> list[PlayListItem]:    
    items = youtube.get_playlist_items(id)
    if not items: return NOT_FOUND
    return items

@router.get("/books", response_model=List[SkillBooks], description="Подбор книг под конкретный навык")
async def search_list_of_books(text: list[str] = QueryTextValidation, count: int = QueryCountValidation, lang: str = QueryLanguageValidation, free: bool = QueryBoolValidation) -> list[SkillBooks]:
    db = await database.connect()
    books = await litres.get_list_of_books(db, text, count, language=lang, free=free)
    await db.close()
    return books