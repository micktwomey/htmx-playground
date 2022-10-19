from sqlalchemy import Column, DateTime, Integer, String, func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from alembic.config import Config
from alembic import command

Base = declarative_base()


def create_session_maker() -> sessionmaker:
    return sessionmaker(expire_on_commit=False, class_=AsyncSession)


SessionMaker = create_session_maker()


async def get_session():
    async with SessionMaker() as session:
        yield session


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)
    create_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, onupdate=func.now(), server_default=func.now())


def run_upgrade(connection, config: Config):
    config.attributes["connection"] = connection
    command.upgrade(config, "head")


async def setup(sqluri: str):
    engine = create_async_engine(sqluri)
    async with engine.begin() as conn:
        await conn.run_sync(run_upgrade, Config("alembic.ini"))
    SessionMaker.configure(bind=engine)


async def get_widgets(session: AsyncSession) -> list[Widget]:
    results = await session.execute(select(Widget))
    return results.scalars().all()


async def create_or_update_widget(session: AsyncSession, key: str, value: str) -> int:
    async with session.begin():
        stmt = select(Widget).filter_by(key=key)
        results = await session.execute(stmt)
        w = results.scalar()
        if w is not None:
            w.value = value
        else:
            w = Widget(key=key, value=value)
            session.add(w)
        await session.commit()
    return w.id
