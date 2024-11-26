from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from uuid import UUID
from datetime import datetime

class TemplateSectionSchema(BaseModel):
    title: str
    questions: List[Dict[str, Any]]

class TemplateCreate(BaseModel):
    title: str
    description: Optional[str] = None
    sections: List[TemplateSectionSchema]
    version: Optional[int] = 1
    is_active: Optional[bool] = True

class TemplateResponse(TemplateCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
