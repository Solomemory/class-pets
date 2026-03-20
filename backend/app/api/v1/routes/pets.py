from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_dependency
from app.schemas.pet import PetTemplateResponse
from app.services.pet_service import PetService

router = APIRouter(prefix='/pet-templates')


@router.get('', response_model=list[PetTemplateResponse])
def list_pet_templates(db: Session = Depends(db_dependency)) -> list[PetTemplateResponse]:
    templates = PetService.list_pet_templates(db)
    return [
        PetTemplateResponse(
            id=template.id,
            name=template.name,
            pet_type=template.pet_type,
            lore=template.lore,
            rarity=template.rarity,
            image_url=template.image_url,
            created_at=template.created_at,
            stage_configs=sorted(template.stage_configs, key=lambda s: s.stage_index),
        )
        for template in templates
    ]
