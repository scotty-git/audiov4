from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional
from uuid import UUID
from datetime import datetime

class QuestionnaireResponseCreate(BaseModel):
    template_id: UUID
    responses: Dict[str, Any]
    status: Optional[str] = 'submitted'

class QuestionnaireResponseResponse(QuestionnaireResponseCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
