from fastapi import APIRouter, Request
from api.validation import *
from models import *
from api import youtube, litres
import re
from urllib.parse import unquote
import database
import asyncio

# db = None
router = APIRouter()

# async def InitDatabase():
#     global db
#     db = await database.connect()



@router.get("/")
async def home():
    return {
        "success": "true",
        "message": "Документация проекта: http://api.edwica.ru/docs"
        }

@router.get("/videos", response_model=list[Video], description="Подбор видео под конкретный навык")
async def search_list_of_videos(text: str = QueryTextValidation, count: int = QueryCountValidation) -> list[Video]:
    videos = youtube.get_list_of_video(text, count)
    return videos

@router.get("/videos/{id}", response_model=VideoDetail, description="Подробная информация о видео")
async def search_video(id: str) -> VideoDetail:
    video = youtube.get_video(id)
    if not video: return NOT_FOUND
    return video

@router.get("/playlists", response_model=list[PlayList], description="Подбор плейлистов под конкретный навык")
async def search_list_of_playlists(text: str = QueryTextValidation, count: int = QueryCountValidation) -> list[PlayList]:
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

@router.get("/books", response_model=list[Book], description="Подбор книг под конкретный навык")
async def search_list_of_books(request: Request, text: str = QueryTextValidation, count: int = QueryCountValidation, lang: str = QueryLanguageValidation) -> list[Book]:
    try:
        text = re.sub(r'text=|&', '', re.findall(r'text=.*?&', request.url.query)[0]) # Пытаемся получить декодированную строку, чтобы не игнорировались знаки по типу +
    except BaseException:
        ...
    db = await database.connect()
    books = await litres.get_list_of_books(db, unquote(text), count, language=lang)
    await db.close()
    return books