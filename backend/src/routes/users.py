from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from models.success import Success
from models.users import UserRead
from utils.db import get_db

router = APIRouter()


@router.post(
    "/create_user/",
    tags=["Users"],
    response_model=Success,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    email_address: str, password: str, session: Session = Depends(get_db)
) -> Success:
    sql_str = sql.text(
        f"""
        INSERT INTO users (email_address, password)
        VALUES ({email_address}, {password});
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()


@router.get(
    "/read_users/",
    tags=["Users"],
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
)
async def read_users(session: Session = Depends(get_db)) -> List[UserRead]:
    sql_str = sql.text(
        """
        SELECT * 
        FROM users;
        """
    )
    result = session.execute(sql_str).fetchall()
    return [UserRead(email_address=i.email_address) for i in result]


@router.post(
    "/update_user/",
    tags=["Users"],
    response_model=Success,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    email_address: str, password, session: Session = Depends(get_db)
) -> Success:
    sql_str = sql.text(
        f"""
        UPDATE users
        SET password = {password}
        WHERE email_address = {email_address};
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()


@router.post(
    "/delete_user/",
    tags=["Users"],
    response_model=Success,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    email_address: str, session: Session = Depends(get_db)
) -> Success:
    sql_str = sql.text(
        f"""
        DELETE
        FROM users
        WHERE email_address = {email_address};
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()
