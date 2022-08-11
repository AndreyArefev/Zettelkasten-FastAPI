from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from src.zettelkasten.tables import idea_child, idea_tags, Idea, Tag, User

config = context.config
section = config.config_ini_section
fileConfig(config.config_file_name)
target_metadata = [User.metadata, Idea.metadata, Tag.metadata]
