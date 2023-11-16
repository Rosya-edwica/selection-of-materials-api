from models import Video, SkillVideos
from api.youtube.config import  get_youtube_data_by_query
from database import find_videos_in_history, save_videos_to_history
import asyncio

async def get_list_of_video(db, query_list: list[str], count: int = 3) -> list[SkillVideos]:
    queries_set = set(query_list)
    videos_from_history = await get_videos_from_history(db, queries_set, count)
    founded_skills = set((i.skill for i in videos_from_history))
    not_founded_skills = queries_set - founded_skills
    videos_from_youtube = await get_videos_from_youtube(db, not_founded_skills, count)
    return videos_from_history + videos_from_youtube


async def get_videos_from_history(db, query_list: set[str], count: int = 3) -> list[SkillVideos]:
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(find_videos_in_history(loop, skill, count)) 
        for skill in query_list]
    videos = [i for i in await asyncio.gather(*tasks) if i is not None]
    return videos

async def get_videos_from_youtube(db, query_list: str, count: int = 3) -> list[SkillVideos]:
    loop = asyncio.get_event_loop()
    tasks = [asyncio.create_task(get_skill_videos(loop, skill, count)) 
        for skill in query_list]
    videos = [i for i in await asyncio.gather(*tasks) if i is not None]
    return videos


async def get_skill_videos(loop, skill_name: str, count: int = 3) -> SkillVideos:
    videos: list[Video] = []
    json_data = await get_youtube_data_by_query(query=skill_name)
    for item in json_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
        if "itemSectionRenderer" not in item.keys(): continue
        
        for video_data in item["itemSectionRenderer"]["contents"]:
            if "videoRenderer" not in video_data.keys():
                continue
            
            video = Video(
                id=video_data["videoRenderer"]["videoId"],
                name=video_data["videoRenderer"]["title"]["runs"][0]["text"],
                link="https://www.youtube.com/watch?v=" + video_data["videoRenderer"]["videoId"],
                header_image=video_data["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
            )
            videos.append(video)
    await save_videos_to_history(loop, skill_name, videos)
    return SkillVideos(
        skill=skill_name,
        materials=videos[:count]
    )
