from models import Video, VideoDetail, SkillVideos
from pyyoutube import Api, error
from contextlib import suppress
from api.youtube.config import TOKEN

domain = "https://www.youtube.com/watch?v="

api = Api(api_key=TOKEN)

def get_list_of_video(queryList: list[str], count: int = 3) -> list[SkillVideos]:
    result: list[SkillVideos] = []
    for skill in queryList:
        result.append(get_skill_videos(skill, count))
    return result

def get_skill_videos(skillName: str, count: int = 3) -> list[SkillVideos]:
    videos: list[Video] = []
    data = api.search_by_keywords(q=skillName, search_type=["video"], count=count, region_code="RU").to_dict()
    if not data["items"]: return []
    for item in data["items"]:
        videos.append(Video(
                id=item["id"]["videoId"],
                name=item["snippet"]["title"],
                link=domain + item["id"]["videoId"],
                header_image=data["snippet"]["thumbnails"]["default"]["url"]
            ))
    return SkillVideos(
        skill=skillName,
        materials=videos[:count])
    

def get_video(id: str) -> VideoDetail | None:
    data: dict = {}
    with suppress(IndexError, error.PyYouTubeException):
        data = api.get_video_by_id(video_id=id).items[0].to_dict()
        video = VideoDetail(
            id=id,
            link=domain + id,
            name=data["snippet"]["title"],
            description=data["snippet"]["description"],
            published_at=data["snippet"]["publishedAt"],       
            header_image=data["snippet"]["thumbnails"]["default"]["url"],
            tags=data["snippet"]["tags"], 
            views=data["statistics"]["viewCount"]
        )
    if not data: return None
    return video