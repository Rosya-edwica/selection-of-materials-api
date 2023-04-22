from fastapi import APIRouter
from api.validation import QueryCountValidation, QueryTextValidation, BAD_REQUEST
from models import *
from api import youtube

router = APIRouter()

@router.get("/videos", response_model=list[Video], description="Noize MC")
async def search_list_of_videos(text: str = QueryTextValidation, count: int = QueryCountValidation) -> list[Video]:
    videos = youtube.get_list_of_video(text, count)
    return videos

@router.get("/videos/{id}", response_model=VideoDetail)
async def search_video(id: str) -> VideoDetail:
    video = youtube.get_video(id)
    if not video: return BAD_REQUEST
    return video

@router.get("/playlists", response_model=list[PlayList])
async def search_list_of_playlists(text: str = QueryTextValidation, count: int = QueryCountValidation) -> list[PlayList]:
    playlists = youtube.get_list_of_playlist(text, count)
    return playlists

@router.get("/playlists/{id}", response_model=PlayListDetail)
async def search_playlist(id: str) -> PlayListDetail:
    playlist = youtube.get_playlist(id) 
    if not playlist: return BAD_REQUEST
    return playlist


@router.get("/playlists/{id}/items", response_model=list[PlayListItem])
async def search_playlist_items(id: str) -> list[PlayListItem]:    
    items = youtube.get_playlist_items(id)
    if not items: return BAD_REQUEST
    return items