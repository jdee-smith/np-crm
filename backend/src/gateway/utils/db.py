import os
from random import choice
from string import digits
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gateway.utils.constants import ID_LEN

DB = os.environ.get("POSTGRES_DB")
USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
HOST = os.environ.get("POSTGRES_HOST")

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB}")


def get_db() -> Generator:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def generate_id() -> str:
    id = "".join(choice(digits) for i in range(ID_LEN))
    return id
