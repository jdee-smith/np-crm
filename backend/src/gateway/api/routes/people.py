from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from gateway.api.models.people import (
    IndividualPerson,
    PeopleCreateRequest,
    PeopleCreateResponse,
    PeopleDeleteRequest,
    PeopleDeleteResponse,
    PeopleReadResponse,
    PeopleUpdateRequest,
    PeopleUpdateResponse,
)
from gateway.utils.db import generate_id, get_db, map_result

router = APIRouter()


@router.post("/create_person/", tags=["People"], response_model=PeopleCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_person(request: PeopleCreateRequest, session: Session = Depends(get_db)) -> PeopleCreateResponse:
    id = generate_id()
    sql_str = sql.text(
        f"""
        INSERT INTO people (id, first_name, last_name)
        VALUES ({id}, '{request.first_name}', '{request.last_name}');
        """
    )
    session.execute(sql_str)
    session.commit()
    return PeopleCreateResponse(id=id)


@router.get("/read_people/", tags=["People"], response_model=PeopleReadResponse, status_code=status.HTTP_200_OK)
async def read_people(session: Session = Depends(get_db)) -> PeopleReadResponse:
    sql_str = sql.text("SELECT * FROM people;")
    cursor = session.execute(sql_str)
    result = map_result(cursor)
    people = [IndividualPerson(**i)for i in result]
    return PeopleReadResponse(people=people)


@router.post("/update_person/", tags=["People"], response_model=PeopleUpdateResponse, status_code=status.HTTP_200_OK)
async def update_person(request: PeopleUpdateRequest, session: Session = Depends(get_db)) -> PeopleUpdateResponse:
    sql_str = sql.text(
        f"""
        UPDATE people
        SET last_updated = CURRENT_TIMESTAMP, first_name = '{request.first_name}', last_name = '{request.last_name}'
        WHERE id = {request.id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return PeopleUpdateResponse(**request)


@router.post("/delete_person/", tags=["People"], response_model=PeopleDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_person(request: PeopleDeleteRequest, session: Session = Depends(get_db)) -> PeopleDeleteResponse:
    sql_str = sql.text(f"DELETE FROM people WHERE id = {request.id};")
    session.execute(sql_str)
    session.commit()
    return PeopleDeleteResponse(**request)
