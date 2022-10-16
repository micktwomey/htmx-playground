import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")

app = fastapi.FastAPI()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


WIDGETS = {"foo": "bar"}


class Widget(BaseModel):
    key: str
    value: str


@app.get("/widgets")
def get_widgets(request: Request):
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": WIDGETS}
    )


@app.post("/widgets")
def post_widget(request: Request, widget: Widget):
    WIDGETS[widget.key] = widget.value
    return templates.TemplateResponse(
        "widgets.html", {"request": request, "widgets": WIDGETS}
    )
