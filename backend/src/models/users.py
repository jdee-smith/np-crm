from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    email_address: str
