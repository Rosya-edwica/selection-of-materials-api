from models import SkillVideos, Video
from database.config import connect

async def save_videos_to_history(loop, skill: str, videos: list[Video]):
    db = await connect(loop)
    async with db.cursor() as cur:
        
        await cur.executemany(f"INSERT IGNORE INTO video(id, name, url, img) VALUES (%s, %s, %s, %s)",
            [(video.id, video.name.replace("'", "`").replace('"', '`'), video.link, video.header_image)
                for video in videos])
        await db.commit()
    await set_connect_between_videos_and_skill(loop, skill, video_ids=[video.id for video in videos])


async def set_connect_between_videos_and_skill(loop, skill: str, video_ids: list[str]):
    db = await connect(loop)
    async with db.cursor() as cur:
        await cur.executemany(f"INSERT IGNORE INTO query_to_video(query, video_id) VALUES(%s, %s);",
            [(skill, video_id) for video_id in video_ids])
        await db.commit()

async def find_videos_in_history(loop, skill: str, limit: int) -> SkillVideos | None:
    query = f"""SELECT video.id, video.name, video.url, video.img 
        FROM video
        INNER JOIN query_to_video ON video.id = query_to_video.video_id
        WHERE LOWER(query_to_video.query) = '{skill.lower().strip()}'
        LIMIT {limit}; """
    
    conn = await connect(loop)
    cursor = await conn.cursor()
    await cursor.execute(query)
    videos = [
            Video(
                id=video[0],
                name=video[1],
                link=video[2],
                header_image=video[3],
            )
            for video in await cursor.fetchall()
    ]
    # async with db.cursor() as cur:
    #     await cur.execute(query)
        
    #     videos = [
    #         Video(
    #             id=video[0],
    #             name=video[1],
    #             link=video[2],
    #             header_image=video[3],
    #         )
    #         for video in await cur.fetchall()
    #     ]
    if videos:
        return SkillVideos(
            skill=skill,
            materials=videos
        )
    return None
