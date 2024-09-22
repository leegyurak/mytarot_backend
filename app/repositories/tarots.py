from sqlalchemy import and_, insert, select

from app.entities import CompatibilityTarotResult, Tarot
from databases import Database


class TarotRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db

    async def get_tarot_by_tarot_id(self, tarot_id: int) -> Tarot | None:
        stmt = select(Tarot).where(Tarot.tarot_id == tarot_id)
        async with self.db.session() as session:
            query = await session.execute(stmt)
        return query.scalars().one_or_none()
    
    
class CompatibilityTarotResultRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        
    async def create_compatibility_tarot_result(
        self,
        first_tarot_id: int,
        second_tarot_id: int,
        commentary: str,
    ) -> None:
        stmt = (
            insert(
                CompatibilityTarotResult,
            ).values(
                first_tarot_id=first_tarot_id,
                second_tarot_id=second_tarot_id,
                commentary=commentary,
            )
        )
        async with self.db.connect() as conn:
            await conn.execute(stmt)
            await conn.commit()
            
    async def get_compatibility_tarot_result_by_first_second_tarot_ids(
        self,
        first_tarot_id: int,
        second_tarot_id: int,
    ) -> CompatibilityTarotResult | None:
        stmt = select(CompatibilityTarotResult).where(
            and_(
                CompatibilityTarotResult.first_tarot_id == first_tarot_id,
                CompatibilityTarotResult.second_tarot_id == second_tarot_id,
            ),
        )
        async with self.db.session() as session:
            query = await session.execute(stmt)
        return query.scalars().one_or_none()
