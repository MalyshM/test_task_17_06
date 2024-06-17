from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from starlette import status
from s3_client import s3_client

meme_router = APIRouter(tags=["memes"], prefix='/memes')


@meme_router.post("/", status_code=status.HTTP_201_CREATED, summary='Добавить мем',
                  description=
                  '''
                  
                  ''')
async def create_item(image: Annotated[bytes, File()], name:str):
    await s3_client.upload_file_bytes(image, name)
    return True

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
