import os
from typing import Annotated, List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from fetch import make_request
from models import connect_db, Meme
from .meme_validators import name_is_exists, id_is_exists
from schemas import MemeScheme, Pagination, PaginationOptions
from .responses import *

load_dotenv()
PRIVATE_API_URL = os.getenv("PRIVATE_API_URL")
S3_SERVER_URL = os.getenv("S3_SERVER_URL")
meme_router = APIRouter(tags=["memes"], prefix='/memes')


@meme_router.post("/", status_code=status.HTTP_201_CREATED, response_model=MemeScheme, summary='Добавить мем',
                  responses={
                      201: resp_201,
                      409: resp_409,
                      500: resp_500
                  },
                  description=
                  '''
                  
                  ''')
async def create_meme(image: Annotated[bytes, File()], name: dict = Depends(name_is_exists),
                      db: AsyncSession = Depends(connect_db)):
    if name['is_exists']:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Meme with that name already exists")
    url = f'{PRIVATE_API_URL}{name["name"]}'
    data = {'image': image}
    response = await make_request(url=url, crud_type=0, data=data)
    print(response)
    db_item = Meme(name=name["name"], link=S3_SERVER_URL + name["name"])
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@meme_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=MemeScheme, summary='Получить мем по id',
                 responses={
                     200: resp_200_one,
                     404: resp_404,
                     500: resp_500
                 }, )
async def read_item(id: int, db: AsyncSession = Depends(connect_db)):
    res = await db.get(Meme, id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404,
                            detail="Meme with that id not found")
    return res


@meme_router.options("/", status_code=status.HTTP_200_OK, response_model=PaginationOptions,
                     summary='Получить количество страниц с указанной пагинацией',
                     responses={
                         200: {
                             "description": "Количество страниц",
                             "content": {
                                 "application/json": {
                                     "example": {
                                         "number_of_pages": 1,
                                         "meme_count": 6
                                     }
                                 }
                             }
                         },
                         500: resp_500
                     }, )
async def count_pages(pagination: Pagination = Depends(), db: AsyncSession = Depends(connect_db)):
    res = await db.execute(text(f"""
        SELECT COUNT(*) FROM meme;
    """))
    res = res.first()[0]
    pages = res // pagination.limit
    if res % pagination.limit != 0:
        pages += 1
    return PaginationOptions(number_of_pages=pages, meme_count=res)


@meme_router.get("/", status_code=status.HTTP_200_OK, response_model=List[MemeScheme],
                 summary='Получить мемы с пагинацией',
                 responses={
                     200: resp_200_many,
                     500: resp_500
                 }, )
async def read_items(pagination: Pagination = Depends(), db: AsyncSession = Depends(connect_db)):
    res = await db.execute(text(f"""
            SELECT * FROM meme
            LIMIT {pagination.limit}
            OFFSET {pagination.offset};
        """))
    res = res.fetchall()
    result = [MemeScheme(**row._asdict()) for row in res]
    return result


@meme_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=MemeScheme, summary='Обновить мем',
                 responses={
                     200: resp_200_one,
                     404: resp_404,
                     409: resp_409,
                     500: resp_500
                 },
                 description=
                 '''

                 ''')
async def update_meme(image: Annotated[bytes, File()], id: dict = Depends(id_is_exists),
                      name: dict = Depends(name_is_exists),
                      db: AsyncSession = Depends(connect_db)):
    if id['is_exists'] is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Meme with that id not found")
    if name['is_exists']:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Meme with that name already exists")
    url = f'{PRIVATE_API_URL}{name["name"]}'
    data = {'image': image}
    response = await make_request(url=url, crud_type=1, data=data)
    print(response)

    db_item = await db.get(Meme, id['id'])
    db_item.name = name["name"]
    db_item.link = S3_SERVER_URL + name["name"]
    await db.commit()
    await db.refresh(db_item)
    return db_item


# todo этот роут и в приватной апишке сделать роут удаления
@meme_router.delete("/{id}", status_code=status.HTTP_200_OK, summary='Удалить мем',
                    responses={
                        200: {
                            "description": "Статус записи",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Meme deleted successfully"
                                    }
                                }
                            }
                        },
                        404: resp_404,
                        500: resp_500
                    },
                    description=
                    '''
   
                    ''')
async def delete_meme(id: dict = Depends(id_is_exists),
                      db: AsyncSession = Depends(connect_db)):
    if id['is_exists'] is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Meme with that id not found")
    meme = await db.get(Meme, id['id'])
    url = f'{PRIVATE_API_URL}{meme.name}'
    response = await make_request(url=url, crud_type=2)
    print(response)
    await db.delete(meme)
    await db.commit()
    return {"message": "Meme deleted successfully"}
