from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.pet import PetStageConfig, PetTemplate
from app.seeds.pet_templates import PET_TEMPLATE_SEED
from app.services.badge_service import BadgeService


def seed_pet_templates(db: Session) -> None:
    for template_data in PET_TEMPLATE_SEED:
        template = db.scalar(
            select(PetTemplate)
            .options(selectinload(PetTemplate.stage_configs))
            .where(PetTemplate.id == template_data['id'])
        )

        if not template:
            template = PetTemplate(
                id=template_data['id'],
                name=template_data['name'],
                pet_type=template_data['pet_type'],
                lore=template_data['lore'],
                rarity=template_data['rarity'],
                image_url=template_data['image_url'],
            )
            db.add(template)
            db.flush()
        else:
            template.name = template_data['name']
            template.pet_type = template_data['pet_type']
            template.lore = template_data['lore']
            template.rarity = template_data['rarity']
            template.image_url = template_data['image_url']
            db.add(template)

        existing_by_index = {stage.stage_index: stage for stage in template.stage_configs}
        target_indexes = {stage['stage_index'] for stage in template_data['stages']}

        for stage_data in template_data['stages']:
            stage = existing_by_index.get(stage_data['stage_index'])
            if not stage:
                stage = PetStageConfig(pet_template_id=template.id, stage_index=stage_data['stage_index'])
                db.add(stage)

            stage.stage_key = stage_data['stage_key']
            stage.stage_name = stage_data['stage_name']
            stage.stage_description = stage_data['stage_description']
            stage.image_prompt = stage_data['image_prompt']
            stage.level_min = stage_data['level_min']
            stage.level_max = stage_data['level_max']

        for idx, stage in existing_by_index.items():
            if idx not in target_indexes:
                db.delete(stage)

    db.commit()


def run_seed(db: Session) -> None:
    seed_pet_templates(db)
    BadgeService.seed_badges(db)
