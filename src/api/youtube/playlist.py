from models import PlayList, SkillPlaylists
from api.youtube.config import  get_youtube_data_by_query
from database import find_playlists_in_history, save_playlists_to_history

async def get_list_of_playlist(db, queryList: list[str], count: int = 3) -> list[SkillPlaylists]:
    result: list[SkillPlaylists] = []
    for skill in queryList:
        playlists_from_history = await find_playlists_in_history(db, skill, count)
        if playlists_from_history:
            result.append(playlists_from_history)
        else:
            playlists = await get_skill_playlists(db, skill, count)
            result.append(playlists)
    return result   


async def get_skill_playlists(db, skill_name: str, count: int = 3) -> list[SkillPlaylists]:
    playlists: list[PlayList] = []
    json_data = await get_youtube_data_by_query(skill_name)
    
    for i in json_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
        if "itemSectionRenderer" not in i.keys(): continue
        for j in i["itemSectionRenderer"]["contents"]:
            if "playlistRenderer" in j.keys():
                video = PlayList(
                    id=j["playlistRenderer"]["playlistId"],
                    name=j["playlistRenderer"]["title"]["simpleText"],
                    link="https://www.youtube.com/watch?v=" + j["playlistRenderer"]["playlistId"],
                    header_image=j["playlistRenderer"]["thumbnails"][0]["thumbnails"][-1]["url"]
                )
                playlists.append(video)
    await save_playlists_to_history(db, skill_name, playlists)
    return SkillPlaylists(
        skill=skill_name,
        materials=playlists[:count]
    )