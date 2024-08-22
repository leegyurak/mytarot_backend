import json
from datetime import datetime

from app.dtos import BirthDateTarotResponseDto
from app.entities import Tarot
from app.exceptions import InvalidDateTimeError, TarotNotFoundError
from app.repositories import TarotRepository
from app.utils import AnthropicProcessor


class TarotService:
    def __init__(self) -> None:
        self._repository: TarotRepository = TarotRepository()

    async def get_birth_date_tarot(self, year: int, month: int, day: int):
        try:
            datetime(year=year, month=month, day=day)
        except ValueError:
            raise InvalidDateTimeError("유효하지 않은 날짜입니다.")
        birth_date_tarot_id: int = 0
        for i in f"{year}{month}{day}":
            birth_date_tarot_id = birth_date_tarot_id + int(i)
        if birth_date_tarot_id > 21:
            birth_date_tarot_id = sum([int(i) for i in str(birth_date_tarot_id)])
        tarot: Tarot | None = await self._repository.get_tarot_by_tarot_id(
            tarot_id=birth_date_tarot_id
        )
        if not tarot:
            raise TarotNotFoundError("해당하는 카드를 찾을 수 없습니다.")
        prompt: str = (
            "너에게 카드의 이름, 설명, 카드의 좋은 의미들, 카드의 나쁜 의미들을 제공 할거야."
            f"1. 카드 이름: {tarot.name[:-2]}"
            f"2. 카드 설명: {tarot.description}"
            f"3. 카드 좋은 의미들: {', '.join(json.dumps(tarot.good_words))}"
            f"4. 카드 나쁜 의미들: {', '.join(json.dumps(tarot.bad_words))}"
            "이 정보들을 바탕으로 문장을 다음과 같은 형식으로 만들어줘"
            "당신의 상징 카드는 (카드 이름)입니다. 이 카드는 (카드 설명을 문장으로 풀어서, 카드 각각의 요소를 해석한 내용을 포함시켜줘)."
            "이 카드를 가진 당신은 (카드의 좋은 의미들) 와 같은 특징을 가지고 있어 (카드의 좋은 의미들을 추상적으로 문장화) 하지만"
            "(카드의 나쁜 의미들) 와 같은 특징도 가지고 있기 때문에 (카드의 나쁜 의미들을 추상적으로 문장화) 하는 점을 (조심해야겠습니다, 주의 해야겠습니다 둘 중 하나 선택)"
        )
        commentary: str = await AnthropicProcessor().get_answer_of_claude(prompt=prompt)
        return BirthDateTarotResponseDto(
            name=tarot.name, img_url=tarot.img_url, commentary=commentary
        )
