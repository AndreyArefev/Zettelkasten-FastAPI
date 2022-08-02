from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)


class Idea(Base):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    idea_name = Column(String)
    idea_text = Column(String)
    tags = relationship("Tag", secondary="idea_tags", back_populates='ideas')
    data_create = Column(Date)
    data_update = Column(Date)
    child_id = Column(Integer, ForeignKey('ideas.id'))


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    tag_name = Column(String)
    ideas = relationship("Idea", secondary="idea_tags", back_populates='tags')


idea_tags = Table('idea_tags', Base.metadata,
    Column('id_idea', ForeignKey('ideas.id'), primary_key=True),
    Column('id_tags', ForeignKey('tags.id'), primary_key=True)
)


