from sqlalchemy import select

from app.entities import Tarot
from databases import Database


class TarotRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db

    async def get_tarot_by_tarot_id(self, tarot_id: int) -> Tarot | None:
        stmt = select(Tarot).where(Tarot.tarot_id == tarot_id)
        async with self.db.session() as session:
            query = await session.execute(stmt)
        return query.scalars().one_or_none()
