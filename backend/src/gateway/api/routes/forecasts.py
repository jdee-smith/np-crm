from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from gateway.api.models.forecasts import ForecastsRead
from gateway.api.models.success import Success
from gateway.utils.db import get_db

router = APIRouter()


@router.get(
    "/read_forecasts/",
    tags=["Forecasts"],
    response_model=List[ForecastsRead],
    status_code=status.HTTP_200_OK,
)
async def read_donations(session: Session = Depends(get_db)) -> List[ForecastsRead]:
    sql_str = sql.text(
        """
        SELECT *
        FROM forecasts;
        """
    )
    result = session.execute(sql_str).fetchall()
    return [
        ForecastsRead(id=i.id, type=i.type, date=i.date, prediction=i.prediction)
        for i in result
    ]
