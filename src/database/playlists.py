from models import SkillPlaylists, PlayList


async def save_playlists_to_history(db, skill: str, playlists: list[PlayList]):
    await db.executemany(f"INSERT INTO playlist(id, name, url, img) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING;", [(playlist.id, playlist.name.replace("'", "`").replace('"', '`'), playlist.link, playlist.header_image) for playlist in playlists])
    await set_connect_between_playlists_and_skill(db, skill, playlists_ids=[playlist.id for playlist in playlists])

async def set_connect_between_playlists_and_skill(db, skill: str, playlists_ids: list[str]):
    await db.executemany(f"INSERT INTO skill_to_playlist(skill, playlist_id) VALUES($1, $2) ON CONFLICT DO NOTHING;", [(skill, playlist_id) for playlist_id in playlists_ids])
    
async def find_playlists_in_history(db, skill: str, limit: int) -> list[SkillPlaylists] | None:
    query = f"""SELECT playlist.id, playlist.name, playlist.url, playlist.img 
        FROM playlist
        INNER JOIN skill_to_playlist ON playlist.id = skill_to_playlist.playlist_id
        WHERE LOWER(skill_to_playlist.skill) = '{skill.lower().strip()}'
        LIMIT {limit}; """
    
    playlists = [
        PlayList(
            id=playlist[0],
            name=playlist[1],
            link=playlist[2],
            header_image=playlist[3],
        )
        for playlist in await db.fetch(query)
    ]
    if playlists:
        return SkillPlaylists(
            skill=skill,
            materials=playlists
        )
    return None