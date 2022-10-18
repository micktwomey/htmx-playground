import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from . import database

templates = Jinja2Templates(directory="templates")

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup_event():
    await database.setup_engine("sqlite+aiosqlite:///fastapi.sqlite")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class Widget(BaseModel):
    key: str
    value: str


@app.get("/widgets")
async def get_widgets(
    request: Request,
    session: database.AsyncSession = fastapi.Depends(database.get_session),
):
    results = await session.execute(database.select(database.Widget))
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": results.scalars().all()}
    )


@app.post("/widgets")
async def post_widget(
    request: Request,
    widget: Widget,
    session: database.AsyncSession = fastapi.Depends(database.get_session),
):
    async with session.begin():
        stmt = database.select(database.Widget).filter_by(key=widget.key)
        results = await session.execute(stmt)
        w = results.scalar()
        if w is not None:
            w.value = widget.value
        else:
            w = database.Widget(key=widget.key, value=widget.value)
            session.add(w)
        await session.commit()
    results = await session.execute(database.select(database.Widget))
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": results.scalars().all()}
    )
