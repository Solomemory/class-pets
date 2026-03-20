from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.models.badge import StudentPetBadge
from app.models.pet import PetTemplate, StudentPet
from app.models.point_log import PointLog
from app.schemas.point import AddPointRequest
from app.services.badge_service import BadgeService
from app.services.growth_service import GrowthService
from app.services.student_service import StudentService


class PointService:
    @staticmethod
    def add_points(db: Session, student_id: int, payload: AddPointRequest) -> tuple[PointLog, StudentPet | None]:
        if payload.point_change == 0:
            raise ValueError('积分变更不能为 0')
        if payload.point_change < 0 and not settings.allow_negative_points:
            raise ValueError('当前系统不允许负积分')

        student = StudentService.get_student_or_404(db, student_id)

        student.total_points = max(0, student.total_points + payload.point_change)
        student.available_points = max(0, student.available_points + payload.point_change)
        db.add(student)

        try:
            student_pet = StudentService.get_student_pet(db, student_id)
        except ValueError:
            student_pet = None

        attribute_delta = (
            GrowthService.calculate_attribute_delta(payload.reason, payload.point_change)
            if student_pet
            else {'wisdom': 0, 'focus': 0, 'affinity': 0, 'resilience': 0, 'vitality': 0}
        )
        if student_pet:
            GrowthService.apply_attribute_delta(student_pet, attribute_delta)

        log = PointLog(
            student_id=student.id,
            point_change=payload.point_change,
            reason=payload.reason,
            remark=payload.remark,
            wisdom_delta=attribute_delta['wisdom'],
            focus_delta=attribute_delta['focus'],
            affinity_delta=attribute_delta['affinity'],
            resilience_delta=attribute_delta['resilience'],
            vitality_delta=attribute_delta['vitality'],
        )
        db.add(log)
        db.flush()

        student_pet = GrowthService.recalculate_student_pet(db, student) if student_pet else None
        if student_pet:
            BadgeService.sync_badges(db, student, student_pet)
            badge_count = len(BadgeService.list_student_pet_badges(db, student_pet.id))
            GrowthService.refresh_meta_fields(db, student, student_pet, badge_count)

        db.commit()

        reloaded_log = db.scalar(select(PointLog).where(PointLog.id == log.id))
        if student_pet is None:
            return reloaded_log, None

        reloaded_pet = db.scalar(
            select(StudentPet)
            .options(
                selectinload(StudentPet.pet_template).selectinload(PetTemplate.stage_configs),
                selectinload(StudentPet.badges).selectinload(StudentPetBadge.badge),
            )
            .where(StudentPet.id == student_pet.id)
        )
        return reloaded_log, reloaded_pet

    @staticmethod
    def list_logs(db: Session, student_id: int | None = None) -> list[PointLog]:
        stmt = select(PointLog).order_by(PointLog.created_at.desc())
        if student_id:
            stmt = stmt.where(PointLog.student_id == student_id)
        return list(db.scalars(stmt).all())
