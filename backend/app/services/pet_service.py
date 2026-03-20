from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.pet import PetTemplate


class PetService:
    @staticmethod
    def list_pet_templates(db: Session) -> list[PetTemplate]:
        stmt = select(PetTemplate).options(selectinload(PetTemplate.stage_configs))
        return list(db.scalars(stmt).all())
