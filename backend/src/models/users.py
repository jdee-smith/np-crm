import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email_address: str
    create_date: datetime.date
    password: str
