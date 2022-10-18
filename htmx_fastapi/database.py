from sqlalchemy import Integer, String, Column, DateTime, func, select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()

SessionMaker = sessionmaker(expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with SessionMaker() as session:
        yield session


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)
    create_date = Column(DateTime, server_default=func.now())


async def setup_engine(sqluri: str):
    engine = create_async_engine("sqlite+aiosqlite:///fastapi.sqlite")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    SessionMaker.configure(bind=engine)
