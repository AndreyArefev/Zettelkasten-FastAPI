from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import (
    models,
    tables,
)
from ..database import get_session


class IdeasService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self, user_id: int) -> List[tables.Idea]:
        ideas = (
            self.session
            .query(tables.Idea)
            .filter(tables.Idea.user_id == user_id)
            .order_by(
                tables.Idea.data_create.desc(),
                tables.Idea.id.desc(),
            )
            .all()
        )
        return ideas

    def get_by_tag(self, user_id: int, tag: str) -> Optional[tables.Tag]:
        ideas = (
            self.session
            .query(tables.Tag)
            .filter(
                tables.Tag.user_id == user_id,
                tables.Tag.tag_name == tag
            )
            .first()
        )
        if not ideas:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return ideas

    def get_by_word(self, user_id: int, word: str) -> List[tables.Idea]:
        ideas = (
            self.session
            .query(tables.Idea)
            .filter(
                tables.Idea.user_id == user_id,
                tables.Idea.idea_text.contains(word)
            )
            .order_by(
                tables.Idea.data_create.desc(),
                tables.Idea.id.desc(),
            )
            .all()
        )
        if not ideas:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return ideas

    def get_by_name(self, user_id: int, name: str) -> List[tables.Idea]:
        ideas = (
            self.session
            .query(tables.Idea)
            .filter(
                tables.Idea.user_id == user_id,
                tables.Idea.idea_name == name
            )
            .order_by(
                tables.Idea.data_create.desc(),
                tables.Idea.id.desc(),
            )
            .first()
        )
        if not ideas:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return ideas


    def get(
        self,
        user_id: int,
        idea_id: int
    ) -> tables.Idea:
        idea = self._get(user_id, idea_id)
        return idea

    def create_idea(
            self,
            user_id: int,
            idea_data: models.IdeaCreate,
    ) -> tables.Idea:
        self.check_unique_name(idea_data.idea_name)
        self.check_not_refer_to_itself(idea_data.idea_name, idea_data.children)
        idea = tables.Idea(
            idea_name = idea_data.idea_name,
            idea_text = idea_data.idea_text,
            data_create = idea_data.data_create,
            user_id=user_id,
        )
        self.tag_get_and_create(
            user_id,
            idea_data,
            idea,
        )
        self.children_get_and_create(
            user_id,
            idea_data,
            idea,
        )
        #можно было сделать одну функцию 'get_and_create' на children и tag что-бы избавится от повторения кода
        #но решил на две разделить для последующей модификации каждой
        self.session.add(idea)
        self.session.commit()
        return idea

    def update(self,
        user_id: int,
        idea_id: int,
        idea_data: models.IdeaUpdate,
    ) -> tables.Idea:
        idea = self._get(user_id, idea_id)
        self.check_unique_name(idea_data.idea_name, idea_id)
        self.check_not_refer_to_itself(idea_data.idea_name, idea_data.children)
        for field, value in idea_data:
            if field == 'tags':
                setattr(idea, field, [])
                self.tag_get_and_create(
                    user_id,
                    idea_data,
                    idea,
                )
            elif field == 'children':
                setattr(idea, field, [])
                self.children_get_and_create(
                    user_id,
                    idea_data,
                    idea,
                )
            else:
                setattr(idea, field, value)
        self.session.commit()
        return idea

    def delete(
        self,
        user_id: int,
        idea_id: int,
    ):
        idea = self._get(user_id, idea_id)
        self.session.delete(idea)
        self.session.commit()

    def _get(self, user_id: int, idea_id: int) -> Optional[tables.Idea]:
        idea = (
            self.session
            .query(tables.Idea)
            .filter(
                tables.Idea.user_id == user_id,
                tables.Idea.id == idea_id,
            )
            .first()
        )
        if not idea:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return idea

    def tag_get_and_create(
            self,
            user_id: int,
            idea_data: models.IdeaCreate,
            idea: tables.Idea,
                ) -> tables.Idea:
        tags = [i.tag_name for i in idea_data.tags]
        for tag_name in tags:
            # Определим существует ли тег
            teg_in_db = (
                self.session
                .query(tables.Tag)
                .filter(
                    tables.Tag.user_id == user_id,
                    tables.Tag.tag_name == tag_name
                )
                .first()
            )
            # если существует, то добавляем к заметке тег
            if teg_in_db:
                idea.tags.append(teg_in_db)
            # если не существует, то добавляем тег в таблицу тегов
            else:
                c = tables.Tag(user_id=user_id, tag_name=tag_name)
                self.session.add(c)
                self.session.flush()
                idea.tags.append(c)
        return idea

    def children_get_and_create(
            self,
            user_id: int,
            idea_data: models.IdeaSchema,
            idea: tables.Idea,
    ) -> tables.Idea:
        children = [i.idea_name for i in idea_data.children]
        for idea_name in children:
            # Определим существует ли заметка
            idea_in_db = (
                self.session
                .query(tables.Idea)
                .filter(
                    tables.Idea.user_id == user_id,
                    tables.Idea.idea_name == idea_name
                )
                .first()
            )
            # если существует, то добавляем к заметке связанную идею
            if idea_in_db:
                idea.children.append(idea_in_db)
            # если не существует, то добавляем пустую идею в таблицу идей
            else:
                if isinstance(idea_data, models.IdeaCreate):
                    data_create = idea_data.data_create
                else:
                    data_create = idea_data.data_update
                c = tables.Idea(user_id=user_id, idea_name=idea_name, idea_text='', data_create=data_create)
                self.session.add(c)
                self.session.flush()
                idea.children.append(c)
        return idea

    def check_unique_name(self, idea_name: str, idea_id = 0): #проверка что имя заметки уникально для выбранного пользователя
        checking = (
            self.session
            .query(tables.User)
            .filter(
                tables.Idea.idea_name == idea_name,
                tables.Idea.id != idea_id,
            )
            .first()
        )
        if checking:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Заметка с таким именем уже существует',
                               )
        return checking

    def check_not_refer_to_itself(self, idea_name: str, children: List[str]): #проверка что заметка не ссылается сама на себя
        child = [i.idea_name for i in children]
        for child_name in child:
            print(child_name)
            if idea_name == child_name:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail='Заметка не может ссылаться сама на себя',
                                    )
        return idea_name

