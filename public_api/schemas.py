from pydantic import BaseModel, Field


class MemeScheme(BaseModel):
    id: int = Field(..., description='id мема')
    name: str = Field(..., description='название файла мема')
    link: str = Field(..., description='ссылка на файл мема')


class Pagination(BaseModel):
    limit: int = Field(..., ge=10, le=100, description='максимальное количество записей на одну стр')
    offset: int = Field(..., ge=0, le=100, description='(стр-1) * limit, чтобы оказаться на нужной стр')


class PaginationOptions(BaseModel):
    number_of_pages: int = Field(..., description='количество страниц')
    meme_count: int = Field(..., description='количество мемов')
