from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from models.donations import DonationsRead
from models.success import Success
from utils.db import generate_id, get_db

router = APIRouter()


@router.post(
    "/create_donation/",
    tags=["Donations"],
    response_model=Success,
    status_code=status.HTTP_201_CREATED,
)
async def create_donation(
    amount: float,
    method: str,
    person_id: List[int] = Query(None),
    session: Session = Depends(get_db),
) -> Success:
    id = generate_id()
    for i in person_id:
        sql_str = sql.text(
            f"""
            INSERT INTO donations (id, person_id, amount, method)
            VALUES ({id}, {i}, {amount}, {method});
            """
        )
        session.execute(sql_str)
        session.commit()
    return Success()


@router.get(
    "/read_donations/",
    tags=["Donations"],
    response_model=List[DonationsRead],
    status_code=status.HTTP_200_OK,
)
async def read_donations(session: Session = Depends(get_db)) -> List[DonationsRead]:
    sql_str = sql.text(
        """
        SELECT *
        FROM donations;
        """
    )
    result = session.execute(sql_str).fetchall()
    return [
        DonationsRead(
            id=i.id,
            person_id=i.person_id,
            date=i.date,
            amount=i.amount,
            method=i.method,
        )
        for i in result
    ]


@router.post(
    "/update_donation/",
    tags=["Donations"],
    response_model=Success,
    status_code=status.HTTP_200_OK,
)
async def update_donation(
    id: int, date: str, amount: float, method: str, session: Session = Depends(get_db)
) -> Success:
    sql_str = sql.text(
        f"""
        UPDATE donations
        SET date = {date}, amount = {amount}, method = {method}
        WHERE id = {id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()


@router.post(
    "/delete_donation/",
    tags=["Donations"],
    response_model=Success,
    status_code=status.HTTP_200_OK,
)
async def delete_donation(id: int, session: Session = Depends(get_db)) -> Success:
    sql_str = sql.text(
        f"""
        DELETE
        FROM donations
        WHERE id = {id};
        """
    )
    session.execute(sql_str)
    session.commit()
    return Success()
