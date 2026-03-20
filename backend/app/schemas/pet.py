from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMBaseModel


class PetStageConfigResponse(ORMBaseModel):
    id: int
    stage_index: int
    stage_key: str
    stage_name: str
    stage_description: str
    image_prompt: str
    level_min: int
    level_max: int | None


class PetTemplateResponse(ORMBaseModel):
    id: int
    name: str
    pet_type: str
    lore: str
    rarity: str
    image_url: str | None
    created_at: datetime
    stage_configs: list[PetStageConfigResponse]


class SelectPetRequest(BaseModel):
    pet_template_id: int = Field(gt=0)


class PetAttributeResponse(BaseModel):
    wisdom: int
    focus: int
    affinity: int
    resilience: int
    vitality: int
    dominant_attribute_key: str
    dominant_attribute_label: str


class BadgeResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str
    rarity: str
    unlocked_at: datetime


class PetTimelineEventResponse(BaseModel):
    event_code: str
    event_name: str
    event_time: datetime
    detail: str


class StudentPetStatusResponse(BaseModel):
    student_pet_id: int
    pet_template_id: int
    pet_name: str
    pet_type: str
    rarity: str
    total_points: int
    level: int
    stage_index: int
    stage_label: str
    stage_star: int
    stage_star_label: str
    route_key: str
    route_label: str
    route_theme: str
    title: str
    status_key: str
    status_label: str

    current_stage_name: str
    current_stage_description: str
    current_image_prompt: str
    points_per_level: int
    points_to_next_level: int
    points_to_next_stage: int
    next_stage_level: int | None
    evolution_switched: bool = False

    attributes: PetAttributeResponse
    unlocked_badge_count: int = 0
    stage_preview: list[PetStageConfigResponse]


class PetArchiveResponse(BaseModel):
    student_id: int
    student_name: str
    grade_class: str | None
    pet_status: StudentPetStatusResponse
    badges: list[BadgeResponse]
    timeline: list[PetTimelineEventResponse]


class GrowthRuleResponse(BaseModel):
    points_per_level: int
    stages: list[dict[str, int | str | None]]
