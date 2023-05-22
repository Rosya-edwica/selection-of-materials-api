from models import Video, SkillVideos
from api.youtube.config import  get_youtube_data_by_query
from database import find_videos_in_history, save_videos_to_history

async def get_list_of_video(db, queryList: list[str], count: int = 3) -> list[SkillVideos]:
    result: list[SkillVideos] = []
    for skill in queryList:
        videos_from_history = await find_videos_in_history(db, skill, count)
        if videos_from_history:
            result.append(videos_from_history)
        else:
            videos = await get_skill_videos(db, skill, count)
            result.append(videos)
    return result


async def get_skill_videos(db, skill_name: str, count: int = 3) -> list[SkillVideos]:
    videos: list[Video] = []
    json_data = get_youtube_data_by_query(query=skill_name)
    for item in json_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
        if "itemSectionRenderer" not in item.keys(): continue
        
        for video_data in item["itemSectionRenderer"]["contents"]:
            if "videoRenderer" not in video_data.keys(): continue
            
            video = Video(
                id=video_data["videoRenderer"]["videoId"],
                name=video_data["videoRenderer"]["title"]["runs"][0]["text"],
                link="https://www.youtube.com/watch?v=" + video_data["videoRenderer"]["videoId"],
                header_image=video_data["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
            )
            videos.append(video)
    await save_videos_to_history(db, skill_name, videos)
    return SkillVideos(
        skill=skill_name,
        materials=videos[:count]
    )