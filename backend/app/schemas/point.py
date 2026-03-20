from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMBaseModel
from app.schemas.pet import StudentPetStatusResponse


class AddPointRequest(BaseModel):
    point_change: int = Field(description='正负积分变更值')
    reason: str = Field(min_length=1, max_length=50)
    remark: str | None = Field(default=None, max_length=500)


class PointLogResponse(ORMBaseModel):
    id: int
    student_id: int
    point_change: int
    reason: str
    remark: str | None
    wisdom_delta: int
    focus_delta: int
    affinity_delta: int
    resilience_delta: int
    vitality_delta: int
    created_at: datetime


class AddPointResponse(BaseModel):
    log: PointLogResponse
    pet_status: StudentPetStatusResponse | None
