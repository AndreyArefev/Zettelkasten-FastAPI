from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class TagBase(BaseModel):
    tag_name: str

    class Config:
        orm_mode = True

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class IdeaBase(BaseModel):
    idea_name: str

    class Config:
        orm_mode = True

class IdeaText(IdeaBase):
    idea_text: str

class IdeaSchema(IdeaText):
    tags: List[TagBase]
    children: List[IdeaBase]


class IdeaCreate(IdeaSchema):
    data_create: Optional[date] = None


class IdeaUpdate(IdeaSchema):
    data_update: Optional[date] = None


class Idea(IdeaUpdate, IdeaCreate):
    id: int



class TagSchema(TagBase):
    ideas: List[Idea]

    class Config:
        orm_mode = True






