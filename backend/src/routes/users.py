from fastapi import APIRouter, Depends
from sqlalchemy import sql
from sqlalchemy.orm import Session

from models.users import User
from utils.db import get_db

router = APIRouter()


@router.get("/users", tags=["Users"], response_model=list[User])
async def read_users(session: Session = Depends(get_db)) -> list[User]:
    sql_str = sql.text("SELECT * FROM users")
    result = session.execute(sql_str).fetchall()
    return [
        User(
            id=i.id,
            email_address=i.email_address,
            create_date=i.create_date,
            password=i.password,
        )
        for i in result
    ]
