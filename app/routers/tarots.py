from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dtos import (
    BirthDateResponseDto,
    BirthDateCompatibilityResponseDto,
)
from app.exceptions import (
    FailedToCreatePromptError,
    InvalidDateTimeError,
    TarotNotFoundError,
)
from configs import settings
from containers import Container

from ..services import TarotService

tarot: APIRouter = APIRouter(prefix=f"{settings.API_PREFIX}tarots")


class BirthDateFilter(BaseModel):
    year: int
    month: int
    day: int


@tarot.get("/birth-date", tags=["tarots"])
@inject
async def birth_date(
    filter: BirthDateFilter = Depends(BirthDateFilter),
    service: TarotService = Depends(Provide[Container.tarot_service]),
) -> BirthDateResponseDto:
    try:
        return await service.get_birth_date_tarot(
            year=filter.year,
            month=filter.month,
            day=filter.day,
        )
    except (
        FailedToCreatePromptError,
        InvalidDateTimeError,
    ) as error:
        raise HTTPException(detail=error.message, status_code=400) from error
    except TarotNotFoundError as error:
        raise HTTPException(detail=error.message, status_code=404) from error


class BirthDateCompatibilityFilter(BaseModel):
    first_name: str
    first_year: int
    first_month: int
    first_day: int
    second_name: str
    second_year: int
    second_month: int
    second_day: int


@tarot.get("/birth-date-compatibility", tags=["tarots"])
@inject
async def birth_date_compatibility(
    filter: BirthDateCompatibilityFilter = Depends(BirthDateCompatibilityFilter),
    service: TarotService = Depends(Provide[Container.tarot_service]),
) -> BirthDateCompatibilityResponseDto:
    try:
        return await service.get_birth_date_compatibility_tarot(
            first_name=filter.first_name,
            first_year=filter.first_year,
            first_month=filter.first_month,
            first_day=filter.first_day,
            second_name=filter.second_name,
            second_year=filter.second_year,
            second_month=filter.second_month,
            second_day=filter.second_day,
        )
    except (
        FailedToCreatePromptError,
        InvalidDateTimeError,
    ) as error:
        raise HTTPException(detail=error.message, status_code=400) from error
    except TarotNotFoundError as error:
        raise HTTPException(detail=error.message, status_code=404) from error
