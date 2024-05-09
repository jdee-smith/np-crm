import datetime

from pydantic import BaseModel


class ForecastsRead(BaseModel):
    id: int
    type: str
    date: datetime.date
    prediction: float
