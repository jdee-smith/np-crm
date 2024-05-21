from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from gateway.api.models.users import (
    IndividualUser,
    UsersCreateRequest,
    UsersCreateResponse,
    UsersDeleteRequest,
    UsersDeleteResponse,
    UsersReadResponse,
    UsersUpdateRequest,
    UsersUpdateResponse,
)
from gateway.utils.db import generate_id, get_db, map_result

router = APIRouter()


@router.post("/create_user/", tags=["Users"], response_model=UsersCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: UsersCreateRequest, session: Session = Depends(get_db)) -> UsersCreateResponse:
    id = generate_id()
    sql_str = sql.text(
        f"""
        INSERT INTO users (id, email_address, password)
        VALUES ({id}, '{request.email_address}', '{request.password}');
        """
    )
    session.execute(sql_str)
    session.commit()
    return UsersCreateResponse(id=id)


@router.get("/read_users/", tags=["Users"], response_model=UsersReadResponse, status_code=status.HTTP_200_OK)
async def read_users(session: Session = Depends(get_db)) -> UsersReadResponse:
    sql_str = sql.text("SELECT * FROM users;")
    cursor = session.execute(sql_str)
    result = map_result(cursor)
    users = [IndividualUser(**i) for i in result]
    return UsersReadResponse(users=users)


@router.post("/update_user/", tags=["Users"], response_model=UsersUpdateResponse, status_code=status.HTTP_200_OK)
async def update_user(request: UsersUpdateRequest, session: Session = Depends(get_db)) -> UsersUpdateResponse:
    sql_str = sql.text(
        f"""
        UPDATE users
        SET last_updated = CURRENT_TIMESTAMP, password = '{request.password}'
        WHERE email_address = '{request.email_address}';
        """
    )
    session.execute(sql_str)
    session.commit()
    return UsersUpdateResponse(**request)


@router.post("/delete_user/", tags=["Users"], response_model=UsersDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_user(request: UsersDeleteRequest, session: Session = Depends(get_db)) -> UsersDeleteResponse:
    sql_str = sql.text("DELETE FROM users WHERE email_address = '{request.email_address}';")
    session.execute(sql_str)
    session.commit()
    return UsersDeleteResponse(**request)
