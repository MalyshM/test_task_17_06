from typing import Annotated
from fastapi import Response
from fastapi import APIRouter, Depends, UploadFile, File
from starlette import status
from s3_client import s3_client

meme_router = APIRouter(tags=["memes"], prefix='/memes')


@meme_router.post("/", status_code=status.HTTP_201_CREATED, summary='Добавить/обновить мем',
                  description=
                  '''
                  
                  ''')
async def create_meme(image: Annotated[bytes, File()], name:str):
    await s3_client.upload_file_bytes(image, name)
    return True


@meme_router.delete("/", status_code=status.HTTP_200_OK, summary='Удалить мем',
                  description=
                  '''

                  ''')
async def delete_meme(name: str):
    await s3_client.delete_file(name)
    return True
# @meme_router.post("/", status_code=status.HTTP_200_OK, summary='Обновить мем',
#                   description=
#                   '''
#
#                   ''')
# async def update_item(image: Annotated[bytes, File()], name: str):
#     await s3_client.(image, name)
#     return True

# Read (GET)
# @meme_router.get("/{name}")
# async def read_item(name: str, response: Response):
#     res = await s3_client.get_file('3stasik.jpg')
#     response.headers["Content-Type"] = "image/jpeg"
#
#     # Return the image as the response
#     response.content = res
#     return response
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
