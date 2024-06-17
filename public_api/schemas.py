from pydantic import BaseModel


class MemeScheme(BaseModel):
    id: int
    name: str
    link: str
