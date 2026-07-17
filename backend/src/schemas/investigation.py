from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class InvestigationBase(BaseModel):
    title: str
    target_data: Dict[str, Any]

class InvestigationCreate(InvestigationBase):
    pass

class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    target_data: Optional[Dict[str, Any]] = None

class InvestigationResponse(InvestigationBase):
    id: int
    status: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
