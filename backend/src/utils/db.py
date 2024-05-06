import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
engine = create_engine(f"postgresql://{user}:{password}@{host}/{db}")


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
