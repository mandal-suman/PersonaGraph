from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.investigation import InvestigationCreate, InvestigationResponse, InvestigationUpdate
from src.services import investigation_service
from src.api.deps import get_current_active_user
from src.models.user import User

router = APIRouter()

@router.get("/", response_model=List[InvestigationResponse])
async def read_investigations(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve investigations for current user.
    """
    investigations = await investigation_service.get_investigations_for_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return investigations

@router.post("/", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED)
async def create_investigation(
    *,
    db: AsyncSession = Depends(get_db),
    investigation_in: InvestigationCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new investigation.
    """
    investigation = await investigation_service.create_investigation(
        db=db, investigation=investigation_in, user_id=current_user.id
    )
    return investigation

@router.get("/{investigation_id}", response_model=InvestigationResponse)
async def read_investigation(
    investigation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get investigation by ID.
    """
    investigation = await investigation_service.get_investigation(
        db=db, investigation_id=investigation_id, user_id=current_user.id
    )
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation

@router.put("/{investigation_id}", response_model=InvestigationResponse)
async def update_investigation(
    investigation_id: int,
    investigation_in: InvestigationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an investigation.
    """
    investigation = await investigation_service.update_investigation(
        db=db, 
        investigation_id=investigation_id, 
        user_id=current_user.id,
        investigation_update=investigation_in
    )
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation

@router.delete("/{investigation_id}")
async def delete_investigation(
    investigation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an investigation.
    """
    success = await investigation_service.delete_investigation(
        db=db, investigation_id=investigation_id, user_id=current_user.id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return {"message": "Investigation deleted successfully"}
