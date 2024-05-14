import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class IndividualForecast(BaseModel):
    id: int = Field()
    type: str = Field()
    series: int = Field()
    sample: Optional[int] = Field(None)
    date: datetime.date = Field()
    forecast: float = Field()


class ForecastsReadResponse(BaseModel):
    forecasts: List[IndividualForecast] = Field()


class ForecastsCreateResponse(BaseModel):
    id: int = Field()


class ForecastsDeleteRequest(BaseModel):
    id: int = Field()


class ForecastsDeleteResponse(BaseModel):
    id: int = Field()
