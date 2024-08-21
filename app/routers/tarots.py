from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dtos import BirthDateTarotResponseDto
from app.exceptions import InvalidDateTimeError, TarotNotFoundError
from app.services import TarotService
from configs import settings

tarot: APIRouter = APIRouter(prefix=f'{settings.API_PREFIX}tarots')


class BirthDateTarotFilter(BaseModel):
    year: int
    month: int
    day: int


@tarot.get('/birth-date-tarot', tags=['tarots'])
async def birth_date_tarot(filter: BirthDateTarotFilter = Depends()) -> BirthDateTarotResponseDto:
    try:
        return await TarotService().get_birth_date_tarot(
            year=filter.year,
            month=filter.month,
            day=filter.day,
        )
    except InvalidDateTimeError as error:
        raise HTTPException(detail=error.message, status_code=400) from error
    except TarotNotFoundError as error:
        raise HTTPException(detail=error.message, status_code=404) from error
