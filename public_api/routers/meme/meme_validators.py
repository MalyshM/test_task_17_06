from sqlalchemy import text
from starlette import status
from starlette.exceptions import HTTPException

from models import async_session


async def is_already_exists(name: str):
    async with async_session() as db:
        is_already_exists = await db.execute(text(f"""
                select 1 
                from meme m 
                where m.name = '{name}'
                limit 1;
            """))
    if is_already_exists.first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Meme with that name already exists")
    return name
