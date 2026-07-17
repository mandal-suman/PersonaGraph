from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.investigation import Investigation
from src.schemas.investigation import InvestigationCreate, InvestigationUpdate

async def get_investigations_for_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Investigation]:
    stmt = select(Investigation).where(Investigation.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_investigation(db: AsyncSession, investigation_id: int, user_id: int) -> Optional[Investigation]:
    stmt = select(Investigation).where(
        Investigation.id == investigation_id,
        Investigation.user_id == user_id
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_investigation(db: AsyncSession, investigation: InvestigationCreate, user_id: int) -> Investigation:
    db_investigation = Investigation(
        title=investigation.title,
        target_data=investigation.target_data,
        user_id=user_id
    )
    db.add(db_investigation)
    await db.commit()
    await db.refresh(db_investigation)
    return db_investigation

async def update_investigation(
    db: AsyncSession,
    investigation_id: int,
    user_id: int,
    investigation_update: InvestigationUpdate
) -> Optional[Investigation]:
    db_investigation = await get_investigation(db, investigation_id, user_id)
    if not db_investigation:
        return None
    
    update_data = investigation_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_investigation, key, value)
        
    await db.commit()
    await db.refresh(db_investigation)
    return db_investigation

async def delete_investigation(db: AsyncSession, investigation_id: int, user_id: int) -> bool:
    db_investigation = await get_investigation(db, investigation_id, user_id)
    if not db_investigation:
        return False
        
    await db.delete(db_investigation)
    await db.commit()
    return True
