from typing import List
from pydantic import BaseModel, Field


class IndividualForecast(BaseModel):
    series: int = Field(examples=[1], gt=0)
    sample: int = Field(examples=[1], gt=0)
    step: int = Field(examples=[1], gt=0)
    value: float = Field(examples=[23.23])


class ForecastRequest(BaseModel):
    prediction_length: int = Field(examples=[3], gt=0)
    context: List[List[float]] = Field(examples=[[[2.0, 3.0], [4.0, 5.0]]])

class ForecastResponse(BaseModel):
    forecasts: List[IndividualForecast] = Field()
