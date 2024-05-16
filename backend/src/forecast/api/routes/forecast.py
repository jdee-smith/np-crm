import os

from chronos import ChronosPipeline
from fastapi import APIRouter, status

from forecast.api.models.forecast import ForecastRequest, ForecastResponse
from forecast.utils.postprocess import postprocess
from forecast.utils.preprocess import preprocess

FORECAST_MODEL = os.environ.get("FORECAST_MODEL")
model = ChronosPipeline.from_pretrained(FORECAST_MODEL)

router = APIRouter()


@router.post(
    "/predict/",
    tags=["Forecast"],
    response_model=ForecastResponse,
    status_code=status.HTTP_200_OK,
)
async def predict(request: ForecastRequest) -> ForecastResponse:
    global model
    processed_context = preprocess(request.context)
    forecasts = model.predict(processed_context, request.prediction_length)
    processed_forecasts = postprocess(forecasts)
    return ForecastResponse(forecasts=processed_forecasts)
