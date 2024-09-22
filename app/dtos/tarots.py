from pydantic import BaseModel, HttpUrl


class BirthDateResponseDto(BaseModel):
    name: str
    img_url: HttpUrl
    commentary: str
    

class _BirthDateWithoutCommentaryDto(BaseModel):
    name: str
    img_url: HttpUrl
    
    
class BirthDateCompatibilityResponseDto(BaseModel):
    first_man: _BirthDateWithoutCommentaryDto
    second_man: _BirthDateWithoutCommentaryDto
    commentary: str
