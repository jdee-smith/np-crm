import datetime

from pydantic import BaseModel


class DonationsRead(BaseModel):
    id: int
    person_id: int
    date: datetime.date
    amount: float
    method: str
