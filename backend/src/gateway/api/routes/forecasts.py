import os

import requests
from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from forecast.api.models.forecast import ForecastRequest, ForecastResponse
from gateway.api.models.forecasts import (
    ForecastsCreateRequest,
    ForecastsCreateResponse,
    ForecastsDeleteRequest,
    ForecastsDeleteResponse,
    ForecastsReadMetricsResponse,
    ForecastsReadResponse,
    IndividualForecast,
    IndividualForecastMetrics,
)
from gateway.utils.constants import FORECAST_URL
from gateway.utils.dates import last_day_of_relative_month_str
from gateway.utils.db import generate_id, get_db, map_result


PREDICTION_URL = os.path.join(FORECAST_URL, "predict")

router = APIRouter()


@router.post("/create_forecast/", tags=["Forecasts"], response_model=ForecastsCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_forecast(request: ForecastsCreateRequest, session: Session = Depends(get_db)) -> ForecastsCreateResponse:
    id = generate_id()
    data_sql_str = sql.text(f"SELECT * FROM {request.table} WHERE month != (SELECT MAX(month) FROM {request.table});")
    ts = session.execute(data_sql_str).fetchall()
    context = [[float(i[1]) for i in ts]]

    settings_sql_str = sql.text("SELECT name, value FROM settings WHERE service = 'Forecast';")
    settings = session.execute(settings_sql_str).fetchall()
    request = ForecastRequest(context=context, **dict(settings))
    response = requests.post(PREDICTION_URL, json=request.dict())
    forecasts = ForecastResponse(forecasts=response.json()["forecasts"])

    for i in forecasts.forecasts:
        date = last_day_of_relative_month_str(ts[-1][0], steps=i.step)
        insert_sql_str = sql.text(
            f"""
            INSERT INTO sample_forecasts (id, type, series, sample, date, forecast)
            VALUES ({id}, 'Donations', {i.series}, {i.sample}, '{date}', ROUND({i.value}, 2));
            """
        )
        session.execute(insert_sql_str)
        session.commit()

    return ForecastsCreateResponse(id=id)


@router.get("/read_forecasts/", tags=["Forecasts"], response_model=ForecastsReadResponse, status_code=status.HTTP_200_OK)
async def read_forecasts(session: Session = Depends(get_db)) -> ForecastsReadResponse:
    sql_str = sql.text("SELECT * FROM forecasts;")
    cursor = session.execute(sql_str)
    result = map_result(cursor)
    forecasts = [IndividualForecast(**i) for i in result]
    return ForecastsReadResponse(forecasts=forecasts)


@router.get("/read_metrics/", tags=["Forecasts"], response_model=ForecastsReadMetricsResponse, status_code=status.HTTP_200_OK)
async def read_metrics(session: Session = Depends(get_db)) -> ForecastsReadMetricsResponse:
    sql_str = sql.text("SELECT * FROM aggregate_forecast_metrics")
    cursor = session.execute(sql_str)
    result = map_result(cursor)
    forecasts = [IndividualForecastMetrics(**i) for i in result]
    return ForecastsReadMetricsResponse(forecasts=forecasts)


@router.post("/delete_forecast/", tags=["Forecasts"], response_model=ForecastsDeleteRequest, status_code=status.HTTP_200_OK)
async def delete_forecast(request: ForecastsDeleteRequest, session: Session = Depends(get_db)) -> ForecastsDeleteResponse:
    sql_str = sql.text(f"DELETE FROM sample_forecasts WHERE id = {request.id};")
    session.execute(sql_str)
    session.commit()
    return ForecastsDeleteResponse(**request)
