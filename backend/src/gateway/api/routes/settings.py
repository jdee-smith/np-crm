from fastapi import APIRouter, Depends, status
from sqlalchemy import sql
from sqlalchemy.orm import Session

from gateway.api.models.settings import (
    IndividualSetting,
    SettingsReadResponse,
    SettingsUpdateRequest,
    SettingsUpdateResponse,
)
from gateway.utils.db import get_db, map_result

router = APIRouter()


@router.get("/read_settings/", tags=["Settings"], response_model=SettingsReadResponse, status_code=status.HTTP_200_OK)
async def read_settings(session: Session = Depends(get_db)) -> SettingsReadResponse:
    sql_str = sql.text("SELECT * FROM settings;")
    cursor = session.execute(sql_str)
    result = map_result(cursor)
    settings = [IndividualSetting(**i) for i in result]
    return SettingsReadResponse(settings=settings)


@router.post("/update_setting/", tags=["Settings"], response_model=SettingsUpdateResponse, status_code=status.HTTP_200_OK)
async def update_setting(request: SettingsUpdateRequest, session: Session = Depends(get_db)) -> SettingsUpdateResponse:
    sql_str = sql.text(
        f"""
        UPDATE settings
        SET last_updated = CURRENT_TIMESTAMP, value = '{request.value}'
        WHERE service = '{request.service}' AND name = '{request.name}';
        """
    )
    session.execute(sql_str)
    session.commit()
    return SettingsUpdateResponse(**request)
