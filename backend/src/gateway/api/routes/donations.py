from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from gateway.api.models.donations import (
    DonationsCreateRequest,
    DonationsCreateResponse,
    DonationsDeleteRequest,
    DonationsDeleteResponse,
    DonationsReadResponse,
    DonationsUpdateRequest,
    DonationsUpdateResponse,
    IndividualDonation,
)
from gateway.utils.db import generate_id, get_db, map_result

router = APIRouter()


@router.post("/create_donation/", tags=["Donations"], response_model=DonationsCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(request: DonationsCreateRequest, session: Session = Depends(get_db)) -> DonationsCreateResponse:
    id = generate_id()
    for i in request.person_id:
        sql_str = sql.text(
            f"""
            INSERT INTO donations (id, person_id, date, amount, method)
            VALUES ({id}, {i}, '{request.date}', {request.amount}, '{request.method}');
            """
        )
        session.execute(sql_str)
        session.commit()
    return DonationsCreateResponse(id=id)


@router.get("/read_donations/", tags=["Donations"], response_model=DonationsReadResponse, status_code=status.HTTP_200_OK)
async def read_donations(session: Session = Depends(get_db)) -> DonationsReadResponse:
    sql_str = sql.text("SELECT * FROM donations;")
    cursor = session.execute(sql_str)
    result = map_result(cursor)
    donations = [IndividualDonation(**i) for i in result]
    return DonationsReadResponse(donations=donations)


@router.post("/update_donation/", tags=["Donations"], response_model=DonationsUpdateResponse, status_code=status.HTTP_200_OK)
async def update_donation(request: DonationsUpdateRequest, session: Session = Depends(get_db)) -> DonationsUpdateResponse:
    sql_str = sql.text(
        f"""
        UPDATE donations
        SET last_updated = CURRENT_TIMESTAMP, date = '{request.date}', amount = {request.amount}, method = '{request.method}'
        WHERE id = {request.id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return DonationsUpdateResponse(**request)


@router.post("/delete_donation/", tags=["Donations"], response_model=DonationsDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_donation(request: DonationsDeleteRequest, session: Session = Depends(get_db)) -> DonationsDeleteResponse:
    sql_str = sql.text("DELETE FROM donations WHERE id = {request.id};")
    session.execute(sql_str)
    session.commit()
    return DonationsDeleteResponse(**request)
