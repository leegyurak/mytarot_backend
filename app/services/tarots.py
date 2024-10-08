import json
import re
from datetime import datetime
from typing import Final

from app.dtos import (
    BirthDateResponseDto,
    BirthDateCompatibilityResponseDto,
)
from app.entities import (
    CompatibilityTarotResult,
    Tarot,
)
from app.exceptions import (
    FailedToCreatePromptError,
    InvalidDateTimeError,
    TarotNotFoundError,
)
from app.repositories import (
    CompatibilityTarotResultRepository,
    TarotRepository,
)
from app.utils import AnthropicProcessor

MAX_TAROT_ID: Final = 21


class TarotService:
    def __init__(
        self,
        tarot_repository: TarotRepository,
        compatibility_tarot_result_repository: CompatibilityTarotResultRepository,
        processor: AnthropicProcessor,
    ) -> None:
        self._tarot_repository = tarot_repository
        self._compatibility_tarot_result_repository = (
            compatibility_tarot_result_repository
        )
        self._processor = processor

    def _validate_date(self, year: int, month: int, day: int) -> None:
        try:
            datetime(year=year, month=month, day=day)
        except ValueError:
            raise InvalidDateTimeError("유효하지 않은 날짜입니다.")

    def _calculate_tarot_id(self, year: int, month: int, day: int) -> int:
        tarot_id: int = sum(int(i) for i in f"{year}{month}{day}")
        while tarot_id > MAX_TAROT_ID:
            tarot_id = sum(int(i) for i in str(tarot_id))
        return tarot_id

    async def _get_tarot_by_date(self, year: int, month: int, day: int) -> Tarot:
        self._validate_date(year=year, month=month, day=day)
        tarot_id: int = self._calculate_tarot_id(year=year, month=month, day=day)
        tarot: Tarot | None = await self._tarot_repository.get_tarot_by_tarot_id(
            tarot_id
        )
        if not tarot:
            raise TarotNotFoundError("해당하는 카드를 찾을 수 없습니다.")
        return tarot

    async def _get_tarots(
        self, first_data: tuple, second_data: tuple
    ) -> tuple[Tarot, Tarot]:
        first_tarot = await self._get_tarot_by_date(*first_data)
        second_tarot = await self._get_tarot_by_date(*second_data)
        return first_tarot, second_tarot

    def _generate_prompt(
        self,
        tarot: Tarot,
        prompt_type: str,
        **kwargs,
    ) -> str:
        if prompt_type == "birth_date":
            return self._generate_birth_date_prompt(tarot)
        elif prompt_type == "compatibility":
            if (
                not kwargs.get("other_tarot")
                or not kwargs.get("first_name")
                or not kwargs.get("second_name")
            ):
                raise FailedToCreatePromptError("정보가 부족합니다.")
            return self._generate_compatibility_prompt(
                tarot,
                kwargs.get("other_tarot"),
                kwargs.get("first_name"),
                kwargs.get("second_name"),
            )
        raise FailedToCreatePromptError("잘못된 prompt_type입니다.")

    def _generate_birth_date_prompt(self, tarot: Tarot) -> str:
        return (
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

    def _generate_compatibility_prompt(
        self, tarot: Tarot, other_tarot: Tarot, first_name: str, second_name: str
    ) -> str:
        return (
            "너에게 두 사람의 이름과 두 사람을 각각 나타내는 두 카드의 이름, 설명, 카드의 좋은 의미들, 카드의 나쁜 의미들을 제공할 거야."
            f"1. 첫 번째 사람 이름: {first_name}"
            f"2. 첫 번째 카드 이름: {tarot.name[:-2]}"
            f"3. 첫 번째 카드 설명: {tarot.description}"
            f"4. 첫 번째 카드 좋은 의미들: {', '.join(json.dumps(tarot.good_words))}"
            f"5. 첫 번째 카드 나쁜 의미들: {', '.join(json.dumps(tarot.bad_words))}"
            f"6. 두 번째 사람 이름: {second_name}"
            f"7. 두 번째 카드 이름: {other_tarot.name[:-2]}"
            f"8. 두 번째 카드 설명: {other_tarot.description}"
            f"9. 두 번째 카드 좋은 의미들: {', '.join(json.dumps(other_tarot.good_words))}"
            f"10. 두 번째 카드 나쁜 의미들: {', '.join(json.dumps(other_tarot.bad_words))}"
            "조건은 다음과 같아"
            "1. 냉정하게 판단해줘, 너 생각에 두 카드가 잘 맞다고 생각이 들지 않는다면 대부분은 보통을 줘."
            "2. 두 카드가 같을 경우에는 무조건 매우 좋음을 줘."
            "3. 카드 이름에 탑, 악마, 죽음이 포함되어 있을 경우 1번보다 더욱 냉정하게 판단해줘."
            "4. 내가 밑에서 요청한 문장 이외의 다른 문장은 말하지마."
            "이 정보들과 조건들을 바탕으로 두 사람의 궁합을 나타내는 문장을 다음과 같이 만들어줘. "
            "(첫 번째 사람 이름)님과 (두 번째 사람 이름)님의 궁합은 (매우 나쁨, 나쁨, 보통, 좋음, 매우 좋음 중 하나 선택)입니다."
            "(첫 번째 사람 이름)님의 상징 카드는 (첫 번째 카드 이름)입니다. 이 카드는 (첫 번째 카드의 해석 및 좋은 의미 나쁜 의미를 간략하게 설명). "
            "(두 번째 사람 이름)님의 상징 카드는 (두 번째 카드 이름)입니다. 이 카드는 (두 번째 카드의 해석 및 좋은 의미 나쁜 의미를 간략하게 설명). "
            "이 두 카드가 만나면서 두 분은 (첫 번째 카드와 두 번째 카드의 긍정적인 의미와 해석들을 조합하여 두 사람이 만났을 때의 시너지를 문장으로 설명)."
            "하지만 두 분은 (첫 번째 카드와 두 번째 카드의 부정적인 의미와 해석들을 조합하여 두 사람이 만났을 때의 악영향를 문장으로 설명)."
            "따라서 이러한 점을 보았을 때, 두 분의 궁합은 (매우 나쁨, 나쁨, 보통, 좋음, 매우 좋음 중 하나 선택)입니다."
        )

    def _masking_name_in_commentary(
        self, commentary: str, first_name: str, second_name: str
    ) -> str:
        if len(second_name) > len(first_name):
            commentary = commentary.replace(second_name, "???")
            commentary = commentary.replace(first_name, "***")
        else:
            commentary = commentary.replace(first_name, "***")
            commentary = commentary.replace(second_name, "???")

        return commentary

    def _unmasking_name_in_commentary(
        self, commentary: str, first_name: str, second_name: str
    ) -> str:
        return commentary.replace("***", first_name).replace("???", second_name)

    async def _generate_compatibility_commentary(
        self, first_tarot: Tarot, first_name: str, second_tarot: Tarot, second_name: str
    ) -> str:
        prompt: str = self._generate_prompt(
            tarot=first_tarot,
            first_name=first_name,
            second_name=second_name,
            other_tarot=second_tarot,
            prompt_type="compatibility",
        )
        commentary: str = await self._processor.get_answer_of_claude(prompt=prompt)
        if first_name != second_name:
            commentary = self._masking_name_in_commentary(
                commentary=commentary,
                first_name=first_name,
                second_name=second_name,
            )

            await self._compatibility_tarot_result_repository.create_compatibility_tarot_result(
                first_tarot_id=first_tarot.id,
                second_tarot_id=second_tarot.id,
                commentary=commentary,
            )
        return commentary

    def _create_compatibility_response(
        self,
        first_tarot: Tarot,
        first_name: str,
        second_tarot: Tarot,
        second_name: str,
        commentary: str,
    ) -> BirthDateCompatibilityResponseDto:
        return BirthDateCompatibilityResponseDto(
            first_man={"name": first_tarot.name, "img_url": first_tarot.img_url},
            second_man={"name": second_tarot.name, "img_url": second_tarot.img_url},
            commentary=(
                self._unmasking_name_in_commentary(
                    commentary=commentary,
                    first_name=first_name,
                    second_name=second_name,
                )
            ),
        )

    async def get_birth_date_tarot(
        self, year: int, month: int, day: int
    ) -> BirthDateResponseDto:
        tarot: Tarot = await self._get_tarot_by_date(year=year, month=month, day=day)
        prompt: str = self._generate_prompt(tarot=tarot, prompt_type="birth_date")
        commentary: str = await self._processor.get_answer_of_claude(prompt=prompt)
        return BirthDateResponseDto(
            name=tarot.name,
            img_url=tarot.img_url,
            commentary=commentary,
        )

    async def get_birth_date_compatibility_tarot(
        self,
        first_name: str,
        first_year: int,
        first_month: int,
        first_day: int,
        second_name: str,
        second_year: int,
        second_month: int,
        second_day: int,
    ) -> BirthDateCompatibilityResponseDto:
        first_tarot, second_tarot = await self._get_tarots(
            (first_year, first_month, first_day),
            (second_year, second_month, second_day),
        )
        compatibility_tarot_result: CompatibilityTarotResult | None = (
            await self._compatibility_tarot_result_repository.get_compatibility_tarot_result_by_first_second_tarot_ids(
                first_tarot_id=first_tarot.id,
                second_tarot_id=second_tarot.id,
            )
        )
        if not compatibility_tarot_result:
            commentary: str = await self._generate_compatibility_commentary(
                first_tarot=first_tarot,
                first_name=first_name,
                second_tarot=second_tarot,
                second_name=second_name,
            )
        return self._create_compatibility_response(
            first_tarot=first_tarot,
            first_name=first_name,
            second_tarot=second_tarot,
            second_name=second_name,
            commentary=(
                compatibility_tarot_result.commentary
                if compatibility_tarot_result
                else commentary
            ),
        )
