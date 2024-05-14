import datetime
from typing import List

from pydantic import BaseModel, Field


class IndividualDonation(BaseModel):
    id: int = Field()
    person_id: int = Field()
    date: datetime.date = Field()
    amount: float = Field
    method: str = Field()


class DonationsReadResponse(BaseModel):
    donations: List[IndividualDonation] = Field()


class DonationsCreateRequest(BaseModel):
    person_id: List[int] = Field()
    date: datetime.date = Field()
    amount: float = Field()
    method: str = Field()


class DonationsCreateResponse(BaseModel):
    id: int = Field()


class DonationsUpdateRequest(BaseModel):
    id: int = Field()
    date: datetime.date = Field()
    amount: float = Field()
    method: str = Field()


class DonationsUpdateResponse(BaseModel):
    id: int = Field()


class DonationsDeleteRequest(BaseModel):
    id: int = Field()


class DonationsDeleteResponse(BaseModel):
    id: int = Field()
