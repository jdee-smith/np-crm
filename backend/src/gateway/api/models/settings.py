from typing import List

from pydantic import BaseModel, Field


class IndividualSetting(BaseModel):
    service: str = Field()
    name: str = Field()
    value: str = Field()


class SettingsReadResponse(BaseModel):
    settings: List[IndividualSetting] = Field


class SettingsUpdateRequest(BaseModel):
    service: str = Field()
    name: str = Field()
    value: str = Field()


class SettingsUpdateResponse(BaseModel):
    service: str = Field()
    name: str = Field()
