from typing import List
from pydantic import BaseModel
from datetime import date


class TagBase(BaseModel):
    tag_name: str


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class IdeaBase(BaseModel):
    idea_name: str
    idea_text: str
    data_create: date
    child_id: int


class IdeaSchema(IdeaBase):
    tags: List[TagBase]


class Idea(IdeaSchema):
    id: int

    class Config:
        orm_mode = True


class TagSchema(TagBase):
    ideas: List[IdeaBase]


class IdeaCreate(IdeaSchema):
    pass

class IdeaUpdate(IdeaSchema):
    data_update: date



