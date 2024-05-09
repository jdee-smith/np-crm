from typing import List

from pydantic import BaseModel


class ForecastRequest(BaseModel):
    prediction_length: int
    context: List[float]


class ForecastResponse(BaseModel):
    predictions: List[float]
