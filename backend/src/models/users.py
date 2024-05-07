from pydantic import BaseModel


class UserRead(BaseModel):
    email_address: str
