from fastapi import APIRouter, status

from forecast.api.models.health import Health

router = APIRouter()


@router.get(
    "/health/", tags=["Health"], status_code=status.HTTP_200_OK, response_model=Health
)
async def service_health() -> Health:
    return Health()
