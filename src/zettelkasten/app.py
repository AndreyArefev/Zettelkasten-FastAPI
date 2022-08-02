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

app.include_router(api.router)
