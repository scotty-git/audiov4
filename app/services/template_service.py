from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateResponse
from app.api.errors import DetailedHTTPException
from loguru import logger
from typing import List, Optional

class TemplateService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_template(self, template: TemplateCreate) -> TemplateResponse:
        try:
            db_template = Template(**template.model_dump())
            self.session.add(db_template)
            await self.session.commit()
            await self.session.refresh(db_template)
            return TemplateResponse.model_validate(db_template)
        except Exception as e:
            logger.exception("Template creation failed")
            await self.session.rollback()
            raise DetailedHTTPException(
                status_code=500,
                detail="Failed to create template",
                internal_error=e
            )
    
    async def get_template_by_id(self, template_id: UUID) -> Optional[TemplateResponse]:
        try:
            result = await self.session.execute(
                select(Template).where(Template.id == template_id)
            )
            template = result.scalar_one_or_none()
            return TemplateResponse.model_validate(template) if template else None
        except Exception as e:
            logger.exception(f"Failed to retrieve template {template_id}")
            raise DetailedHTTPException(
                status_code=404,
                detail=f"Template {template_id} not found",
                internal_error=e
            )
    
    async def list_templates(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[TemplateResponse]:
        try:
            result = await self.session.execute(
                select(Template).offset(skip).limit(limit)
            )
            templates = result.scalars().all()
            return [TemplateResponse.model_validate(t) for t in templates]
        except Exception as e:
            logger.exception("Failed to list templates")
            raise DetailedHTTPException(
                status_code=500,
                detail="Failed to retrieve templates",
                internal_error=e
            )
