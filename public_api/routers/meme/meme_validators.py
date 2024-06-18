from sqlalchemy import text
from starlette import status
from starlette.exceptions import HTTPException

from models import async_session


async def name_is_exists(name: str) -> dict:
    async with async_session() as db:
        is_already_exists = await db.execute(text(f"""
                select 1 
                from meme m 
                where m.name = '{name}'
                limit 1;
            """))
    is_exists = False
    if is_already_exists.first() is not None:
        is_exists = True
    return {'name': name, 'is_exists': is_exists}


async def id_is_exists(id: int) -> dict:
    async with async_session() as db:
        is_already_exists = await db.execute(text(f"""
                select 1 
                from meme m 
                where m.id = {id}
                limit 1;
            """))
    is_exists = False
    if is_already_exists.first() is not None:
        is_exists = True
    return {'id': id, 'is_exists': is_exists}