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
    engine = create_async_engine(sqluri)
    async with engine.begin() as conn:
        # TODO: use alembic
        await conn.run_sync(Base.metadata.create_all)
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
