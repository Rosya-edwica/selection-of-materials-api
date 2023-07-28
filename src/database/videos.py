from models import SkillVideos, Video


async def save_videos_to_history(db, skill: str, videos: list[Video]):
    await db.executemany(f"INSERT INTO video(id, name, url, img) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING;",
                         [(video.id, video.name.replace("'", "`").replace('"', '`'), video.link, video.header_image)
                          for video in videos])
    await set_connect_between_videos_and_skill(db, skill, video_ids=[video.id for video in videos])


async def set_connect_between_videos_and_skill(db, skill: str, video_ids: list[str]):
    await db.executemany(f"INSERT INTO skill_to_video(skill, video_id) VALUES($1, $2) ON CONFLICT DO NOTHING;",
                         [(skill, video_id) for video_id in video_ids])


async def find_videos_in_history(db, skill: str, limit: int) -> SkillVideos | None:
    query = f"""SELECT video.id, video.name, video.url, video.img 
        FROM video
        INNER JOIN skill_to_video ON video.id = skill_to_video.video_id
        WHERE LOWER(skill_to_video.skill) = '{skill.lower().strip()}'
        LIMIT {limit}; """
    
    videos = [
        Video(
            id=video[0],
            name=video[1],
            link=video[2],
            header_image=video[3],
        )
        for video in await db.fetch(query)
    ]
    if videos:
        return SkillVideos(
            skill=skill,
            materials=videos
        )
    return None
