from typing import List

from pydantic import BaseModel, Field


class IndividualForecast(BaseModel):
    series: int = Field()
    sample: int = Field()
    step: int = Field()
    value: float = Field


class ForecastRequest(BaseModel):
    prediction_length: int = Field()
    context: List[List[float]] = Field()


class ForecastResponse(BaseModel):
    forecasts: List[IndividualForecast] = Field()
