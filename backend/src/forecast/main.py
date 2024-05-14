from fastapi import APIRouter, FastAPI

from forecast.api.routes import forecast, health

router = APIRouter()
router.include_router(health.router)
router.include_router(forecast.router)

app = FastAPI()
app.include_router(router)
