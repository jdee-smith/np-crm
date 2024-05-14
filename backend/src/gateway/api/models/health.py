from pydantic import BaseModel, Field


class Health(BaseModel):
    status: str = Field(default="OK")
