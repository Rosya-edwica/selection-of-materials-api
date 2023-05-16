from models import PlayList, PlayListDetail, PlayListItem, SkillPlaylists
from pyyoutube import Api, error
from contextlib import suppress
from api.youtube.config import TOKEN



domain = "https://www.youtube.com/playlist?list="

api = Api(api_key=TOKEN)

def get_list_of_playlist(queryList: list[str], count: int = 3) -> list[SkillPlaylists]:
    result: list[SkillPlaylists] = []
    for skill in queryList:
        result.append(get_skill_playlists(skill, count))
    return result   

def get_skill_playlists(skillName: str, count: int = 3) -> SkillPlaylists:
    playlists: list[PlayList] = []
    with suppress(IndexError, error.PyYouTubeException):
        data = api.search_by_keywords(q=skillName, search_type=["playlist"], count=count, region_code="RU").to_dict()
        for item in data["items"]:  
            playlists.append(PlayList(  
                id=item["id"]["playlistId"],    
                name=item["snippet"]["title"], 
                link=domain + item["id"]["playlistId"]   
            ))  
    return SkillPlaylists(
        skill=skillName,
        materials=playlists[:count]
    )


def get_playlist(id: str) -> PlayListDetail:
    data = api.get_playlist_by_id(playlist_id=id).to_dict()["items"]
    if not data: return None

    return PlayListDetail(
        id=id,
        name=data[0]["snippet"]["title"],
        description=data[0]["snippet"]["description"],
        published_at=data[0]["snippet"]["publishedAt"],
        link=domain + id,
        header_image=data[0]["snippet"]["thumbnails"]["default"]["url"],
        items_count=data[0]["contentDetails"]["itemCount"]
    )

def get_playlist_items(id: str) -> list[PlayListItem]:
    items: list[PlayListItem] = []
    with suppress(IndexError, error.PyYouTubeException):
        data = api.get_playlist_items(playlist_id=id).to_dict()
        if not data["items"]: return []
        
        items, _ = get_items_from_page(playlist_id=id)
        next_page = data["nextPageToken"]
        while next_page:
            page_items, next_page = get_items_from_page(playlist_id=id, page_token=next_page)
            items += page_items        
    return items

def get_items_from_page(playlist_id: str, page_token: str = None) -> tuple[list[PlayListItem], str]:
    items: list[PlayListItem] = []
    with suppress(IndexError, error.PyYouTubeException):
        data = api.get_playlist_items(playlist_id=playlist_id, page_token=page_token).to_dict()
        if not data["items"]: return []

        playlist_data = data["items"]
        for item in playlist_data:
            if item["status"]["privacyStatus"] != "public": continue
            video_id = item["contentDetails"]["videoId"]
            items.append(PlayListItem(
                id=video_id,
                link=f"https://www.youtube.com/watch?v={video_id}&list={id}",
                name=item["snippet"]["title"],
                description=item["snippet"]["description"],
                published_at=item["contentDetails"]["videoPublishedAt"],
                header_image=item["snippet"]["thumbnails"]["default"]["url"]
            ))
        return items, data["nextPageToken"]