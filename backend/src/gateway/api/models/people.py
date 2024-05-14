from typing import List

from pydantic import BaseModel, Field


class IndividualPerson(BaseModel):
    id: int = Field()
    first_name: str = Field()
    last_name: str = Field()


class PeopleReadResponse(BaseModel):
    people: List[IndividualPerson] = Field()


class PeopleCreateRequest(BaseModel):
    first_name: str = Field()
    last_name: str = Field()


class PeopleCreateResponse(BaseModel):
    id: int = Field()


class PeopleUpdateRequest(BaseModel):
    id: int = Field()
    first_name: str = Field()
    last_name: str = Field()


class PeopleUpdateResponse(BaseModel):
    id: int = Field()


class PeopleDeleteRequest(BaseModel):
    id: int = Field()


class PeopleDeleteResponse(BaseModel):
    id: int = Field()
