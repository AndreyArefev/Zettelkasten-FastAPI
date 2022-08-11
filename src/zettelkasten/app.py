from fastapi import FastAPI

from . import api


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },
{
        'name': 'ideas',
        'description': 'Создание, просмотр, редактирование и удаление заметок',
    },
]

app = FastAPI(
    title='zettelkasten',
    description='Zettelkasten',
    openapi_tags=tags_metadata,
)

@app.get("/")
def read_root():
    return {"Zettelkasten": "http://127.0.0.1:5000/docs/"}

app.include_router(api.router)
