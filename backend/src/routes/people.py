from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from models.people import PeopleRead
from models.success import Success
from utils.db import generate_id, get_db

router = APIRouter()


@router.post(
    "/create_person/",
    tags=["People"],
    response_model=Success,
    status_code=status.HTTP_201_CREATED,
)
async def create_person(
    first_name: str, last_name: str, session: Session = Depends(get_db)
) -> Success:
    id = generate_id()
    sql_str = sql.text(
        f"""
        INSERT INTO people (id, first_name, last_name)
        VALUES ({id}, {first_name}, {last_name});
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()


@router.get(
    "/read_people/",
    tags=["People"],
    response_model=List[PeopleRead],
    status_code=status.HTTP_200_OK,
)
async def read_people(session: Session = Depends(get_db)) -> List[PeopleRead]:
    sql_str = sql.text(
        """
        SELECT *
        FROM people;
        """
    )
    result = session.execute(sql_str).fetchall()
    return [
        PeopleRead(id=i.id, first_name=i.first_name, last_name=i.last_name)
        for i in result
    ]


@router.post(
    "/update_person/",
    tags=["People"],
    response_model=Success,
    status_code=status.HTTP_200_OK,
)
async def update_person(
    id: int, first_name: str, last_name: str, session: Session = Depends(get_db)
) -> Success:
    sql_str = sql.text(
        f"""
        UPDATE people
        SET first_name = {first_name}, last_name = {last_name}
        WHERE id = {id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()


@router.post(
    "/delete_person/",
    tags=["People"],
    response_model=Success,
    status_code=status.HTTP_200_OK,
)
async def delete_person(id: int, session: Session = Depends(get_db)) -> Success:
    sql_str = sql.text(
        f"""
        DELETE
        FROM people
        WHERE id = {id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()
