from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import db_dependency
from app.schemas.point import AddPointRequest, AddPointResponse, PointLogResponse
from app.services.growth_service import GrowthService
from app.services.point_service import PointService
from app.services.student_service import StudentService

router = APIRouter()


@router.post('/students/{student_id}/points', response_model=AddPointResponse)
def add_points(
    student_id: int,
    payload: AddPointRequest,
    db: Session = Depends(db_dependency),
) -> AddPointResponse:
    try:
        student = StudentService.get_student_or_404(db, student_id)
        log, student_pet = PointService.add_points(db, student_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    pet_status = GrowthService.build_status_dto(student, student_pet, db=db) if student_pet else None
    return AddPointResponse(log=PointLogResponse.model_validate(log), pet_status=pet_status)


@router.get('/point-logs', response_model=list[PointLogResponse])
def list_point_logs(
    student_id: int | None = Query(default=None),
    db: Session = Depends(db_dependency),
) -> list[PointLogResponse]:
    logs = PointService.list_logs(db, student_id)
    return [PointLogResponse.model_validate(log) for log in logs]
