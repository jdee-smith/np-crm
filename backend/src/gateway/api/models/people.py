from pydantic import BaseModel


class PeopleRead(BaseModel):
    id: int
    first_name: str
    last_name: str
