import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB = os.environ.get("POSTGRES_DB")
USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
HOST = os.environ.get("POSTGRES_HOST")

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB}")


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
