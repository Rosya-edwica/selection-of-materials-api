from fastapi import APIRouter
from typing import List

from api.validation import *
from models import *
import database
from api import youtube, litres, vacancies
import asyncio

router = APIRouter()

loop = asyncio.get_event_loop()

@router.get("/")
async def home():
    return {
        "success": "true",
        "message": "Документация проекта: http://api.edwica.ru/docs"
        }


@router.get("/videos", response_model=list[SkillVideos], description="Подбор видео под конкретный навык")
async def search_list_of_videos(text: List[str] = QueryTextValidation, count: int = QueryCountValidation) \
        -> list[SkillVideos]:
    db = await database.connect(loop)
    videos = await youtube.get_list_of_video(db, text, count)
    return videos


@router.get("/playlists", response_model=list[SkillPlaylists], description="Подбор плейлистов под конкретный навык")
async def search_list_of_playlists(text: List[str] = QueryTextValidation, count: int = QueryCountValidation) \
        -> list[SkillPlaylists]:
    db = await database.connect(loop)
    playlists = await youtube.get_list_of_playlist(db, text, count)
    return playlists


@router.get("/books", response_model=List[SkillBooks], description="Подбор книг под конкретный навык")
async def search_list_of_books(text: list[str] = QueryTextValidation, count: int = QueryCountValidation,
                               lang: str = QueryLanguageValidation, free: bool = QueryBoolValidation) -> list[SkillBooks]:
    db = await database.connect(loop)
    books = await litres.get_list_of_books(db, text, count, language=lang, free=free)
    return books


@router.get("/vacancies", response_model=List[ProfessionVacancies], description="Поиск вакансий на Superjob/TrudVsem/Geekjob")
async def search_list_of_vacancies(text: list[str] = QueryTextValidation, count: int = 3, platform: str = None,
                                   city: str = None) -> list[ProfessionVacancies]:
    platform = platform.lower().strip() if platform else None
    items = await vacancies.find_vacancies(text, count, platform, city)
    return items
