# htmx-playground

Playing around with [Htmx](https://htmx.org/) and [FastAPI](https://fastapi.tiangolo.com/)

To run:

1. `poetry install`
2. `poetry run uvicorn main:app --reload`
3. Go to [http://localhost:8000/](http://localhost:8000/)
   1. Try adding something, it should reload after the POST
   2. Try watching with dev tools to see what's happening
