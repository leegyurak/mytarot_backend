from pydantic import AnyUrl, BaseModel


class BirthDateTarotResponseDto(BaseModel):
    name: str
    img_url: AnyUrl
    commentary: str
