from fastapi import APIRouter, FastAPI

from routes import health, users

router = APIRouter()
router.include_router(health.router)
router.include_router(users.router)

app = FastAPI()
app.include_router(router)
