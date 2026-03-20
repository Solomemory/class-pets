from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMBaseModel
from app.schemas.pet import StudentPetStatusResponse


class StudentCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    grade_class: str | None = Field(default=None, max_length=50)


class StudentResponse(ORMBaseModel):
    id: int
    name: str
    grade_class: str | None
    total_points: int
    available_points: int
    created_at: datetime


class StudentListItemResponse(StudentResponse):
    pet_status: StudentPetStatusResponse | None = None


class StudentDetailResponse(StudentResponse):
    pet_status: StudentPetStatusResponse | None = None
