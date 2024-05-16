from fastapi import APIRouter, status

from forecast.api.models.root import Root

router = APIRouter()


@router.get("/", tags=["Root"], status_code=status.HTTP_200_OK, response_model=Root)
async def root() -> Root:
    return Root()
