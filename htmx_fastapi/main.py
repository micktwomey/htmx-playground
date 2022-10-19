import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import jinja2

from . import database

templates = Jinja2Templates(
    directory="templates",
    loader=jinja2.PackageLoader(package_name="htmx_fastapi", package_path="templates"),
)

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
    widgets = await database.get_widgets(session)
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": widgets}
    )


@app.post("/widgets")
async def post_widget(
    request: Request,
    widget: Widget,
    session: database.AsyncSession = fastapi.Depends(database.get_session),
):
    await database.create_or_update_widget(session, key=widget.key, value=widget.value)
    widgets = await database.get_widgets(session)
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": widgets}
    )
