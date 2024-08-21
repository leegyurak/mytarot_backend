from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils.types.url import URLType

from app.entities.base import TimeStampBase


class Tarot(TimeStampBase):
    __tablename__ = 'tarots'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(31), nullable=False)
    description: Mapped[str] = mapped_column(String(2047), nullable=False)
    good_words: Mapped[str] = mapped_column(String(255), nullable=False)
    bad_words: Mapped[str] = mapped_column(String(255), nullable=False)
    tarot_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    img_url: Mapped[URLType] = mapped_column(URLType, nullable=False)
