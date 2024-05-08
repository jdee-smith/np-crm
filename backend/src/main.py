from fastapi import APIRouter, FastAPI

from routes import donations, health, people, users

router = APIRouter()
router.include_router(health.router)
router.include_router(users.router)
router.include_router(people.router)
router.include_router(donations.router)

app = FastAPI()
app.include_router(router)
