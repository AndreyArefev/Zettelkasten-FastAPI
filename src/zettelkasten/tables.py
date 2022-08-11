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


Base = declarative_base() #создание базового класса для всех таблиц и классов с ними связанными


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password_hash = Column(String)

idea_child = Table('idea_child', Base.metadata,
    Column('id_idea_parent', ForeignKey('ideas.id'), primary_key=True),
    Column('id_idea_child', ForeignKey('ideas.id'), primary_key=True)
)

class Idea(Base):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    idea_name = Column(String(255))
    idea_text = Column(String)
    tags = relationship("Tag", secondary="idea_tags", back_populates='ideas')
    data_create = Column(Date)
    data_update = Column(Date)
    children = relationship('Idea',
                            secondary=idea_child,
                            primaryjoin=id == idea_child.c.id_idea_parent,
                            secondaryjoin=id == idea_child.c.id_idea_child,
                            backref="idea_parent"
                            )


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    tag_name = Column(String(100))
    ideas = relationship("Idea", secondary="idea_tags", back_populates='tags')


idea_tags = Table('idea_tags', Base.metadata,
    Column('id_idea', ForeignKey('ideas.id'), primary_key=True),
    Column('id_tags', ForeignKey('tags.id'), primary_key=True)
)



