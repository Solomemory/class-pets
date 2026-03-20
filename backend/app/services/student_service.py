from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.models.badge import StudentPetBadge
from app.models.pet import PetStageConfig, PetTemplate, StudentPet
from app.models.point_log import PointLog
from app.models.student import Student
from app.schemas.pet import (
    BadgeResponse,
    PetArchiveResponse,
    PetTimelineEventResponse,
    SelectPetRequest,
)
from app.schemas.student import StudentCreateRequest
from app.services.badge_service import BadgeService
from app.services.growth_service import GrowthService


class StudentService:
    @staticmethod
    def _student_query():
        return (
            select(Student)
            .options(
                selectinload(Student.pet)
                .selectinload(StudentPet.pet_template)
                .selectinload(PetTemplate.stage_configs),
                selectinload(Student.pet)
                .selectinload(StudentPet.badges)
                .selectinload(StudentPetBadge.badge),
            )
        )

    @staticmethod
    def _get_pet_template_with_base_stage(db: Session, pet_template_id: int) -> tuple[PetTemplate, PetStageConfig]:
        pet_template = db.scalar(
            select(PetTemplate)
            .options(selectinload(PetTemplate.stage_configs))
            .where(PetTemplate.id == pet_template_id)
        )
        if not pet_template:
            raise ValueError('宠物模板不存在')

        base_stage = next((cfg for cfg in pet_template.stage_configs if cfg.stage_index == 1), None)
        if not base_stage:
            raise ValueError('宠物模板缺少初始形态配置')
        return pet_template, base_stage

    @staticmethod
    def create_student(db: Session, payload: StudentCreateRequest) -> Student:
        student = Student(name=payload.name, grade_class=payload.grade_class, total_points=0, available_points=0)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def list_students(db: Session) -> list[Student]:
        return list(db.scalars(StudentService._student_query()).all())

    @staticmethod
    def get_student_or_404(db: Session, student_id: int) -> Student:
        student = db.scalar(StudentService._student_query().where(Student.id == student_id))
        if not student:
            raise ValueError('学生不存在')
        return student

    @staticmethod
    def select_pet(db: Session, student_id: int, payload: SelectPetRequest) -> StudentPet:
        student = StudentService.get_student_or_404(db, student_id)
        if student.pet:
            raise ValueError('该学生已经绑定了主宠物')

        pet_template, base_stage = StudentService._get_pet_template_with_base_stage(db, payload.pet_template_id)

        student_pet = StudentPet(
            student_id=student.id,
            pet_template_id=pet_template.id,
            level=1,
            stage_index=1,
            stage_star=1,
            growth_route='starlight',
            growth_title='星辉执律者',
            current_status='stable',
            current_stage_name=base_stage.stage_name,
            current_stage_description=base_stage.stage_description,
            current_image_prompt=base_stage.image_prompt,
            points_to_next_level=GrowthService.calc_points_to_next_level(student.total_points),
            points_to_next_stage=GrowthService.calc_points_to_next_stage(student.total_points, 1),
            next_stage_level=GrowthService.get_next_stage_level(1),
        )
        db.add(student_pet)
        db.flush()
        GrowthService.recalculate_student_pet(db, student)

        BadgeService.sync_badges(db, student, student_pet)
        badge_count = len(BadgeService.list_student_pet_badges(db, student_pet.id))
        GrowthService.refresh_meta_fields(db, student, student_pet, badge_count)
        db.commit()

        return db.scalar(
            select(StudentPet)
            .options(
                selectinload(StudentPet.pet_template).selectinload(PetTemplate.stage_configs),
                selectinload(StudentPet.badges).selectinload(StudentPetBadge.badge),
            )
            .where(StudentPet.id == student_pet.id)
        )

    @staticmethod
    def reselect_pet(db: Session, student_id: int, payload: SelectPetRequest) -> StudentPet:
        student = StudentService.get_student_or_404(db, student_id)
        pet_template, base_stage = StudentService._get_pet_template_with_base_stage(db, payload.pet_template_id)

        # 重选宠物：清空培养数据（积分与积分流水），并重置主宠。
        student.total_points = 0
        student.available_points = 0
        db.add(student)

        db.execute(delete(PointLog).where(PointLog.student_id == student.id))

        if student.pet:
            db.delete(student.pet)
            db.flush()

        student_pet = StudentPet(
            student_id=student.id,
            pet_template_id=pet_template.id,
            level=1,
            stage_index=1,
            stage_star=1,
            growth_route='starlight',
            growth_title='星辉执律者',
            current_status='stable',
            current_stage_name=base_stage.stage_name,
            current_stage_description=base_stage.stage_description,
            current_image_prompt=base_stage.image_prompt,
            points_to_next_level=GrowthService.calc_points_to_next_level(student.total_points),
            points_to_next_stage=GrowthService.calc_points_to_next_stage(student.total_points, 1),
            next_stage_level=GrowthService.get_next_stage_level(1),
        )
        db.add(student_pet)
        db.flush()
        GrowthService.recalculate_student_pet(db, student)

        BadgeService.sync_badges(db, student, student_pet)
        badge_count = len(BadgeService.list_student_pet_badges(db, student_pet.id))
        GrowthService.refresh_meta_fields(db, student, student_pet, badge_count)
        db.commit()

        return db.scalar(
            select(StudentPet)
            .options(
                selectinload(StudentPet.pet_template).selectinload(PetTemplate.stage_configs),
                selectinload(StudentPet.badges).selectinload(StudentPetBadge.badge),
            )
            .where(StudentPet.id == student_pet.id)
        )

    @staticmethod
    def get_student_pet(db: Session, student_id: int) -> StudentPet:
        student_pet = db.scalar(
            select(StudentPet)
            .options(
                selectinload(StudentPet.pet_template).selectinload(PetTemplate.stage_configs),
                selectinload(StudentPet.badges).selectinload(StudentPetBadge.badge),
            )
            .where(StudentPet.student_id == student_id)
        )
        if not student_pet:
            raise ValueError('学生尚未绑定宠物')
        return student_pet

    @staticmethod
    def recalculate(db: Session, student_id: int) -> StudentPet:
        student = StudentService.get_student_or_404(db, student_id)
        student_pet = GrowthService.recalculate_student_pet(db, student)
        if not student_pet:
            raise ValueError('学生尚未绑定宠物')

        BadgeService.sync_badges(db, student, student_pet)
        badge_count = len(BadgeService.list_student_pet_badges(db, student_pet.id))
        GrowthService.refresh_meta_fields(db, student, student_pet, badge_count)

        db.commit()
        return db.scalar(
            select(StudentPet)
            .options(
                selectinload(StudentPet.pet_template).selectinload(PetTemplate.stage_configs),
                selectinload(StudentPet.badges).selectinload(StudentPetBadge.badge),
            )
            .where(StudentPet.id == student_pet.id)
        )

    @staticmethod
    def delete_student(db: Session, student_id: int) -> None:
        student = StudentService.get_student_or_404(db, student_id)
        db.delete(student)
        db.commit()

    @staticmethod
    def list_pet_badges(db: Session, student_id: int) -> list[BadgeResponse]:
        student_pet = StudentService.get_student_pet(db, student_id)
        records = BadgeService.list_student_pet_badges(db, student_pet.id)
        return BadgeService.to_badge_response(records)

    @staticmethod
    def get_pet_archive(db: Session, student_id: int) -> PetArchiveResponse:
        student = StudentService.get_student_or_404(db, student_id)
        student_pet = StudentService.get_student_pet(db, student_id)
        badge_records = BadgeService.list_student_pet_badges(db, student_pet.id)
        badge_responses = BadgeService.to_badge_response(badge_records)

        timeline: list[PetTimelineEventResponse] = [
            PetTimelineEventResponse(
                event_code='pet_obtained',
                event_name='契约建立',
                event_time=student_pet.created_at,
                detail=f'获得主宠 {student_pet.pet_template.name}',
            )
        ]

        if student_pet.first_level_up_at:
            timeline.append(
                PetTimelineEventResponse(
                    event_code='first_level_up',
                    event_name='首次升级',
                    event_time=student_pet.first_level_up_at,
                    detail='完成首次等级提升',
                )
            )
        if student_pet.first_evolution_at:
            timeline.append(
                PetTimelineEventResponse(
                    event_code='first_evolution',
                    event_name='首次进化',
                    event_time=student_pet.first_evolution_at,
                    detail='进入进化形态',
                )
            )
        if student_pet.first_super_evolution_at:
            timeline.append(
                PetTimelineEventResponse(
                    event_code='first_super_evolution',
                    event_name='首次超进化',
                    event_time=student_pet.first_super_evolution_at,
                    detail='进入超进化形态',
                )
            )
        if student_pet.ultimate_evolution_at:
            timeline.append(
                PetTimelineEventResponse(
                    event_code='ultimate_evolution',
                    event_name='究极进化达成',
                    event_time=student_pet.ultimate_evolution_at,
                    detail='进入究极进化形态',
                )
            )

        for badge in badge_responses:
            timeline.append(
                PetTimelineEventResponse(
                    event_code=f'badge_{badge.code}',
                    event_name='徽章解锁',
                    event_time=badge.unlocked_at,
                    detail=f'解锁徽章：{badge.name}',
                )
            )

        timeline.sort(key=lambda x: x.event_time)

        status = GrowthService.build_status_dto(student, student_pet, db=db, badge_records=badge_records)
        return PetArchiveResponse(
            student_id=student.id,
            student_name=student.name,
            grade_class=student.grade_class,
            pet_status=status,
            badges=badge_responses,
            timeline=timeline,
        )
