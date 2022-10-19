import logging

import coloredlogs
import jinja2
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from . import database

LOG = logging.getLogger(__name__)

templates = Jinja2Templates(
    directory="templates",
    loader=jinja2.PackageLoader(package_name="htmx_fastapi", package_path="templates"),
)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    LOG.info("startup begin")
    coloredlogs.install(level="INFO")
    LOG.info("coloredlogs installed")
    await database.setup("sqlite+aiosqlite:///fastapi.sqlite")
    LOG.info("startup complete")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class Widget(BaseModel):
    key: str
    value: str


@app.get("/widgets", response_class=HTMLResponse)
async def get_widgets(
    request: Request,
    session: database.AsyncSession = Depends(database.get_session),
):
    widgets = await database.get_widgets(session)
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": widgets}
    )


@app.post("/widgets", response_class=HTMLResponse)
async def post_widget(
    request: Request,
    widget: Widget,
    session: database.AsyncSession = Depends(database.get_session),
):
    await database.create_or_update_widget(session, key=widget.key, value=widget.value)
    widgets = await database.get_widgets(session)
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": widgets}
    )
