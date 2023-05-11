from fastapi import APIRouter
from api.validation import *
from models import *
from api import youtube, litres

router = APIRouter()

@router.get("/")
async def home():
    return {
        "success": "true",
        "message": "Документация проекта: http://127.0.0.1:8000/docs"
        }

@router.get("/videos", response_model=list[Video], description="Подбор видео под конкретный навык")
async def search_list_of_videos(text: str = QueryTextValidation, count: int = QueryCountValidation) -> list[Video]:
    videos = youtube.get_list_of_video(text, count)
    return videos

@router.get("/videos/{id}", response_model=VideoDetail, description="Подробная информация о видео")
async def search_video(id: str) -> VideoDetail:
    video = youtube.get_video(id)
    if not video: return BAD_REQUEST
    return video

@router.get("/playlists", response_model=list[PlayList], description="Подбор плейлистов под конкретный навык")
async def search_list_of_playlists(text: str = QueryTextValidation, count: int = QueryCountValidation) -> list[PlayList]:
    playlists = youtube.get_list_of_playlist(text, count)
    return playlists

@router.get("/playlists/{id}", response_model=PlayListDetail, description="Подробная информация о плейлисте")
async def search_playlist(id: str) -> PlayListDetail:
    playlist = youtube.get_playlist(id) 
    if not playlist: return BAD_REQUEST
    return playlist


@router.get("/playlists/{id}/items", response_model=list[PlayListItem], description="Список видео, принадлежащих плейлисту")
async def search_playlist_items(id: str) -> list[PlayListItem]:    
    items = youtube.get_playlist_items(id)
    if not items: return BAD_REQUEST
    return items

@router.get("/books", response_model=list[Book], description="Подбор книг под конкретный навык")
async def search_list_of_books(text: str = QueryTextValidation, count: int = QueryCountValidation, lang: str = QueryLanguageValidation) -> list[Book]:
    books = litres.get_list_of_books(text, count, language=lang)
    return books