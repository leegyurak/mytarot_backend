from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from databases import Base


class TimeStampBase(Base):
    __abstract__ = True

    created_dt: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone(timedelta(hours=9))),
    )
    updated_dt: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone(timedelta(hours=9))),
        onupdate=lambda: datetime.now(timezone(timedelta(hours=9))),
    )
