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

    def get_by_tag(self, user_id: int, tag: str) -> List[tables.Tag]:
        ideas = (
            self.session
            .query(tables.Tag)
            .filter(
                tables.Tag.user_id == user_id,
                tables.Tag.tag_name == tag
            )
            .order_by(tables.Tag.id.desc())
            .all()
        )
        if not tag:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return ideas

    def get_by_word(self, user_id: int, word: str) -> List[tables.Idea]:
        ideas = (
            self.session
            .query(tables.Idea)
            .filter(
                tables.Idea.user_id == user_id,
                tables.Idea.idea_text.in_(word)
            )
            .order_by(
                tables.Idea.date.desc(),
                tables.Idea.id.desc(),
            )
            .all()
        )
        return ideas

    def get(
        self,
        user_id: int,
        idea_id: int
    ) -> tables.Idea:
        idea = self._get(user_id, idea_id)
        return idea

    def create(
        self,
        user_id: int,
        idea_data: models.IdeaCreate,
    ) -> tables.Idea:
        idea = tables.Idea(
            **idea_data.dict(),
            user_id=user_id,
        )
        self.session.add(idea)
        self.session.commit()
        return idea

    def update(self,
        user_id: int,
        idea_id: int,
        idea_data: models.IdeaUpdate,
    ) -> tables.Idea:
        idea = self._get(user_id, idea_id)
        for field, value in idea_data:
            setattr(idea, field, value)
        self.session.commit()
        return idea

    def delete(
        self,
        user_id: int,
        idea_id: int,
    ):
        operation = self._get(user_id, idea_id)
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