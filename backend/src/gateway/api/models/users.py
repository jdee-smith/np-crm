from typing import List

from pydantic import BaseModel, Field


class IndividualUser(BaseModel):
    id: int = Field()
    email_address: str = Field()


class UsersReadResponse(BaseModel):
    users: List[IndividualUser] = Field()


class UsersCreateRequest(BaseModel):
    email_address: str = Field()
    password: str = Field()


class UsersCreateResponse(BaseModel):
    id: int = Field()


class UsersUpdateRequest(BaseModel):
    email_address: str = Field()
    password: str = Field()


class UsersUpdateResponse(BaseModel):
    email_address: str = Field()


class UsersDeleteRequest(BaseModel):
    email_address: str = Field()


class UsersDeleteResponse(BaseModel):
    email_address: str = Field()
