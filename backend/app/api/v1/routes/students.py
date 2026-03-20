from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import db_dependency
from app.schemas.pet import BadgeResponse, PetArchiveResponse, SelectPetRequest, StudentPetStatusResponse
from app.schemas.student import StudentCreateRequest, StudentDetailResponse, StudentListItemResponse, StudentResponse
from app.services.growth_service import GrowthService
from app.services.student_service import StudentService

router = APIRouter(prefix='/students')


@router.post('', response_model=StudentResponse)
def create_student(payload: StudentCreateRequest, db: Session = Depends(db_dependency)) -> StudentResponse:
    student = StudentService.create_student(db, payload)
    return StudentResponse.model_validate(student)


@router.get('', response_model=list[StudentListItemResponse])
def list_students(db: Session = Depends(db_dependency)) -> list[StudentListItemResponse]:
    students = StudentService.list_students(db)
    result: list[StudentListItemResponse] = []
    for student in students:
        pet_status = None
        if student.pet:
            pet_status = GrowthService.build_status_dto(student, student.pet, db=db)
        result.append(
            StudentListItemResponse(
                id=student.id,
                name=student.name,
                grade_class=student.grade_class,
                total_points=student.total_points,
                available_points=student.available_points,
                created_at=student.created_at,
                pet_status=pet_status,
            )
        )
    return result


@router.get('/{student_id}', response_model=StudentDetailResponse)
def get_student(student_id: int, db: Session = Depends(db_dependency)) -> StudentDetailResponse:
    try:
        student = StudentService.get_student_or_404(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    pet_status = None
    if student.pet:
        pet_status = GrowthService.build_status_dto(student, student.pet, db=db)

    return StudentDetailResponse(
        id=student.id,
        name=student.name,
        grade_class=student.grade_class,
        total_points=student.total_points,
        available_points=student.available_points,
        created_at=student.created_at,
        pet_status=pet_status,
    )


@router.delete('/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(db_dependency)) -> Response:
    try:
        StudentService.delete_student(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/{student_id}/select-pet', response_model=StudentPetStatusResponse)
def select_pet(
    student_id: int,
    payload: SelectPetRequest,
    db: Session = Depends(db_dependency),
) -> StudentPetStatusResponse:
    try:
        student = StudentService.get_student_or_404(db, student_id)
        student_pet = StudentService.select_pet(db, student_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return GrowthService.build_status_dto(student, student_pet, db=db)


@router.post('/{student_id}/reselect-pet', response_model=StudentPetStatusResponse)
def reselect_pet(
    student_id: int,
    payload: SelectPetRequest,
    db: Session = Depends(db_dependency),
) -> StudentPetStatusResponse:
    try:
        student = StudentService.get_student_or_404(db, student_id)
        student_pet = StudentService.reselect_pet(db, student_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return GrowthService.build_status_dto(student, student_pet, db=db)


@router.get('/{student_id}/pet', response_model=StudentPetStatusResponse)
def get_student_pet(student_id: int, db: Session = Depends(db_dependency)) -> StudentPetStatusResponse:
    try:
        student = StudentService.get_student_or_404(db, student_id)
        student_pet = StudentService.get_student_pet(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return GrowthService.build_status_dto(student, student_pet, db=db)


@router.get('/{student_id}/pet/badges', response_model=list[BadgeResponse])
def get_student_pet_badges(student_id: int, db: Session = Depends(db_dependency)) -> list[BadgeResponse]:
    try:
        return StudentService.list_pet_badges(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get('/{student_id}/pet-archive', response_model=PetArchiveResponse)
def get_pet_archive(student_id: int, db: Session = Depends(db_dependency)) -> PetArchiveResponse:
    try:
        return StudentService.get_pet_archive(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post('/{student_id}/recalculate', response_model=StudentPetStatusResponse)
def recalculate_pet(student_id: int, db: Session = Depends(db_dependency)) -> StudentPetStatusResponse:
    try:
        student = StudentService.get_student_or_404(db, student_id)
        student_pet = StudentService.recalculate(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return GrowthService.build_status_dto(student, student_pet, db=db)
