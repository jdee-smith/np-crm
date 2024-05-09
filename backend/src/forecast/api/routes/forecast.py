import os

from chronos import ChronosPipeline
from fastapi import APIRouter, status

from forecast.api.models.forecast import ForecastRequest, ForecastResponse
from forecast.utils.postprocess import postprocess
from forecast.utils.preprocess import preprocess

MODEL = os.environ.get("FORECASTING_MODEL")
model = ChronosPipeline.from_pretrained(MODEL)

router = APIRouter()


@router.post(
    "/predict/",
    tags=["Forecast"],
    response_model=ForecastResponse,
    status_code=status.HTTP_200_OK,
)
async def predict(data: ForecastRequest) -> ForecastResponse:
    global model
    processed_context = preprocess(data.context)
    preds = model.predict(processed_context, data.prediction_length)
    processed_preds = postprocess(preds)
    return ForecastResponse(predictions=processed_preds)
