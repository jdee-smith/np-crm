import datetime
from typing import List, Literal, Dict, Optional

from pydantic import BaseModel, Field

from gateway.utils.mappings import forecast_type_table_mapping


class IndividualForecast(BaseModel):
    id: int = Field()
    type: str = Field()
    series: int = Field()
    date: datetime.date = Field()
    values: Dict[str, float] = Field()


class IndividualForecastMetrics(BaseModel):
    id: int = Field()
    metrics: Dict[str, Optional[float]] = Field()


class ForecastsReadResponse(BaseModel):
    forecasts: List[IndividualForecast] = Field()


class ForecastsReadMetricsResponse(BaseModel):
    forecasts: List[IndividualForecastMetrics] = Field()


class ForecastsCreateRequest(BaseModel):
    type: Literal["donations"] = Field()

    @property
    def table(self):
        return forecast_type_table_mapping[self.type]


class ForecastsCreateResponse(BaseModel):
    id: int = Field()


class ForecastsDeleteRequest(BaseModel):
    id: int = Field()


class ForecastsDeleteResponse(BaseModel):
    id: int = Field()
