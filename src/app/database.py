import os

from databases import Database

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

mindmap = Table(
    "mindmap",
    metadata,
    Column("uuid", Integer, primary_key=True, autoincrement=True),
    Column("id", String),
    Column("leaf", String, nullable=True),
    Column("leaf_message", String, nullable=True),
)

database = Database(DATABASE_URL)
