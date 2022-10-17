# htmx-playground

Playing around with [Htmx](https://htmx.org/), [Django](https://www.djangoproject.com) and [FastAPI](https://fastapi.tiangolo.com/)

To run the FastAPI version:

1. `poetry install`
2. `poetry run uvicorn main:app --reload`
3. Go to [http://localhost:8000/](http://localhost:8000/)
   1. Try adding something, it should reload after the POST
   2. Try watching with dev tools to see what's happening


To run the Django version:

1. `poetry install`
2. `poetry run python manage.py migrate`
3. `poetry run python manage.py runserver`
4. Go to [http://localhost:8000/](http://localhost:8000/)
   1. Try adding something, it should reload after the POST
   2. Try watching with dev tools to see what's happening
   3. You can edit via [http://localhost:8000/admin](http://localhost:8000/admin) (you'll need to create a superuser using `poetry run python manage.py createsuperuser`)
