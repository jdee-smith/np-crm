from pydantic import BaseModel, Field


class Root(BaseModel):
    service_name: str = Field(default="Forecast")
