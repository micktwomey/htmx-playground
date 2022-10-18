import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.asyncio

templates = Jinja2Templates(directory="templates")

app = fastapi.FastAPI()

Base = sqlalchemy.orm.declarative_base()

SessionMaker = sqlalchemy.orm.sessionmaker(
    expire_on_commit=False, class_=sqlalchemy.ext.asyncio.AsyncSession
)


async def get_session():
    async with SessionMaker() as session:
        yield session


class Widget(Base):
    __tablename__ = "widgets"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    key = sqlalchemy.Column(sqlalchemy.String, unique=True)
    value = sqlalchemy.Column(sqlalchemy.String)
    create_date = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.func.now()
    )


@app.on_event("startup")
async def startup_event():
    engine = sqlalchemy.ext.asyncio.create_async_engine(
        "sqlite+aiosqlite:///fastapi.sqlite"
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    SessionMaker.configure(bind=engine)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class WidgetRequest(BaseModel):
    key: str
    value: str


@app.get("/widgets")
async def get_widgets(
    request: Request,
    session: sqlalchemy.ext.asyncio.AsyncSession = fastapi.Depends(get_session),
):
    results = await session.execute(sqlalchemy.select(Widget))
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": results.scalars().all()}
    )


@app.post("/widgets")
async def post_widget(
    request: Request,
    widget: WidgetRequest,
    session: sqlalchemy.ext.asyncio.AsyncSession = fastapi.Depends(get_session),
):
    async with session.begin():
        stmt = sqlalchemy.select(Widget).filter_by(key=widget.key)
        results = await session.execute(stmt)
        w = results.scalar()
        if w is not None:
            w.value = widget.value
        else:
            w = Widget(key=widget.key, value=widget.value)
            session.add(w)
        await session.commit()
    results = await session.execute(sqlalchemy.select(Widget))
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": results.scalars().all()}
    )
