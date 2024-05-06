from fastapi import APIRouter, status

from models.healthcheck import HealthCheck

router = APIRouter()


@router.get(
    "/health",
    tags=["Healthcheck"],
    summary="Perform a health check.",
    response_description="Return HTTP Status Code 200 (OK).",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def service_health() -> HealthCheck:
    return HealthCheck(status="OK")
