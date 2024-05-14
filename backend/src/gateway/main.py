from fastapi import APIRouter, FastAPI

from gateway.api.routes import donations, forecasts, health, people, settings, users

router = APIRouter()
router.include_router(health.router)
router.include_router(users.router)
router.include_router(people.router)
router.include_router(donations.router)
router.include_router(forecasts.router)
router.include_router(settings.router)

app = FastAPI()
app.include_router(router)
