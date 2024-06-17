from sqlalchemy import BigInteger, Column, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/meme"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def connect_db() -> AsyncSession:
    async with async_session() as session:
        yield session


class Meme(Base):
    __tablename__ = 'meme'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('meme_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
