import os

import httpx
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from forecast.api.models.forecast import ForecastRequest, ForecastResponse
from gateway.api.models.forecasts import (
    ForecastsCreateResponse,
    ForecastsDeleteRequest,
    ForecastsDeleteResponse,
    ForecastsReadResponse,
    IndividualForecast,
)
from gateway.utils.constants import FORECAST_URL
from gateway.utils.db import generate_id, get_db

PREDICTION_URL = os.path.join(FORECAST_URL, "predict")

router = APIRouter()


@router.post(
    "/create_forecast/donations/",
    tags=["Forecasts"],
    response_model=ForecastsCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_forecast(
    session: Session = Depends(get_db),
) -> ForecastsCreateResponse:
    id = generate_id()
    data_sql_str = sql.text(
        f"""
        SELECT *
        FROM monthly_donation_amount_expanded
        WHERE month != (SELECT MAX(month) FROM monthly_donation_amount_expanded);
        """
    )
    ts = session.execute(data_sql_str).fetchall()
    context = [[float(i[1]) for i in ts]]

    settings_sql_str = sql.text(
        f"""
        SELECT name, value
        FROM settings
        WHERE service = 'Forecast';
        """
    )
    settings = session.execute(settings_sql_str).fetchall()
    request = ForecastRequest(context=context, **dict(settings))
    response = httpx.post(PREDICTION_URL, json=request.dict())
    forecasts = ForecastResponse(forecasts=response.json()["forecasts"])

    for i in forecasts.forecasts:
        date = (ts[-1][0] + relativedelta(months=i.step)).strftime("%Y-%m-%d")
        insert_sql_str = sql.text(
            f"""
            INSERT INTO sample_forecasts (id, type, series, sample, date, forecast)
            VALUES ({id}, 'Donations', {i.series}, {i.sample}, '{date}', ROUND({i.value}, 2));
            """
        )
        session.execute(insert_sql_str)
        session.commit()

    return ForecastsCreateResponse(id=id)


@router.get(
    "/read_forecasts/",
    tags=["Forecasts"],
    response_model=ForecastsReadResponse,
    status_code=status.HTTP_200_OK,
)
async def read_sample_forecasts(
    session: Session = Depends(get_db),
) -> ForecastsReadResponse:
    sql_str = sql.text(
        """
        SELECT *
        FROM sample_forecasts;
        """
    )
    result = session.execute(sql_str).fetchall()
    forecasts = [
        IndividualForecast(
            id=i.id,
            type=i.type,
            series=i.series,
            sample=i.sample,
            date=i.date,
            forecast=i.forecast,
        )
        for i in result
    ]
    return ForecastsReadResponse(forecasts=forecasts)


@router.get(
    "/read_forecasts/point/",
    tags=["Forecasts"],
    response_model=ForecastsReadResponse,
    status_code=status.HTTP_200_OK,
)
async def read_point_forecasts(
    session: Session = Depends(get_db),
) -> ForecastsReadResponse:
    sql_str = sql.text(
        """
        SELECT *
        FROM point_forecasts;
        """
    )
    result = session.execute(sql_str).fetchall()
    forecasts = [
        IndividualForecast(
            id=i.id, type=i.type, series=i.series, date=i.date, forecast=i.forecast
        )
        for i in result
    ]
    return ForecastsReadResponse(forecasts=forecasts)


@router.get(
    "/read_forecasts/quantile/",
    tags=["Forecasts"],
    response_model=ForecastsReadResponse,
    status_code=status.HTTP_200_OK,
)
async def read_quantile_forecasts(
    quantile: float, session: Session = Depends(get_db)
) -> ForecastsReadResponse:
    sql_str = sql.text(
        f"""
        SELECT *
        FROM quantile_forecasts
        WHERE quantile = {quantile};
        """
    )
    result = session.execute(sql_str).fetchall()
    forecasts = [
        IndividualForecast(
            id=i.id, type=i.type, series=i.series, date=i.date, forecast=i.forecast
        )
        for i in result
    ]
    return ForecastsReadResponse(forecasts=forecasts)


@router.post(
    "/delete_forecast/",
    tags=["Forecasts"],
    response_model=ForecastsDeleteRequest,
    status_code=status.HTTP_200_OK,
)
async def delete_forecast(
    request: ForecastsDeleteRequest, session: Session = Depends(get_db)
) -> ForecastsDeleteResponse:
    sql_str = sql.text(
        f"""
        DELETE
        FROM sample_forecasts
        WHERE id = {request.id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return ForecastsDeleteResponse(id=request.id)
