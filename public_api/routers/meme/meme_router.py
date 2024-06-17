from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from fetch import make_request
from models import connect_db, Meme
from routers.meme.meme_validators import is_already_exists
from schemas import MemeScheme

meme_router = APIRouter(tags=["memes"], prefix='/memes')


@meme_router.post("/", status_code=status.HTTP_201_CREATED, response_model=MemeScheme, summary='Добавить мем',
                  responses={
                      201: {
                          "description": "Мем успешно добавлен",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "id": 1,
                                      "name": "Example Meme",
                                      "link": "https://example.com/meme.jpg"
                                  }
                              }
                          }
                      },
                      409: {
                          "description": "Мем уже существует",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "detail": "Meme with that name already exists"
                                  }
                              }
                          }
                      },
                      500: {
                          "description": "Внутренняя ошибка сервера",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "detail": "internal server error"
                                  }
                              }
                          }
                      }
                  },
                  description=
                  '''
                  
                  ''')
async def create_item(image: Annotated[bytes, File()], name: str = Depends(is_already_exists),
                      db: AsyncSession = Depends(connect_db)):
    url = f'http://localhost:8091/memes?name={name}'
    data = {'image': image}
    response = await make_request(url=url, crud_type=0, data=data)
    print(response)
    db_item = Meme(name=name, link=name)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# Read (GET)
# @meme_router.get("/items/{item_id}")
# async def read_item(item_id: int):
#     db = SessionLocal()
#     item = db.query(Item).filter(Item.id == item_id).first()
#     return item
#
#
# # Update (PUT)
# @meme_router.put("/items/{item_id}")
# async def update_item(item_id: int, name: str, description: str):
#     db = SessionLocal()
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     db_item.name = name
#     db_item.description = description
#     db.commit()
#     return db_item
#
#
# # Delete (DELETE)
# @meme_router.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     db = SessionLocal()
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     db.delete(db_item)
#     db.commit()
#     return {"message": "Item deleted successfully"}
