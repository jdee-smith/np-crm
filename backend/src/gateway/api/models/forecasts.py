import datetime
from typing import List, Literal, Dict, Optional

from pydantic import BaseModel, Field

from gateway.utils.mappings import forecast_type_table_mapping


class IndividualForecast(BaseModel):
    id: int = Field()
    type: str = Field()
    series: int = Field()
    date: datetime.date = Field()
    mean: float = Field()
    p5: float = Field()
    p10: float = Field()
    p20: float = Field()
    p30: float = Field()
    p40: float = Field()
    p50: float = Field()
    p60: float = Field()
    p70: float = Field()
    p80: float = Field()
    p90: float = Field()
    p95: float = Field


class IndividualForecastMetrics(BaseModel):
    id: int = Field()
    mse: Optional[float] = Field()
    mql_p5: Optional[float] = Field()
    mql_p10: Optional[float] = Field()
    mql_p20: Optional[float] = Field()
    mql_p30: Optional[float] = Field()
    mql_p40: Optional[float] = Field()
    mql_p50: Optional[float] = Field()
    mql_p60: Optional[float] = Field()
    mql_p70: Optional[float] = Field()
    mql_p80: Optional[float] = Field()
    mql_p90: Optional[float] = Field()
    mql_p95: Optional[float] = Field()


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
