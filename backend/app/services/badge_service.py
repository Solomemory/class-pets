from datetime import date, datetime, timedelta

from sqlalchemy import distinct, select
from sqlalchemy.orm import Session, selectinload

from app.models.badge import Badge, StudentPetBadge
from app.models.pet import StudentPet
from app.models.point_log import PointLog
from app.models.student import Student
from app.schemas.pet import BadgeResponse
from app.seeds.badges import BADGE_SEED


class BadgeService:
    @staticmethod
    def seed_badges(db: Session) -> None:
        existing = {item.code: item for item in db.scalars(select(Badge)).all()}
        for data in BADGE_SEED:
            badge = existing.get(data['code'])
            if not badge:
                badge = Badge(code=data['code'])
                db.add(badge)

            badge.name = data['name']
            badge.description = data['description']
            badge.rarity = data['rarity']

        db.commit()

    @staticmethod
    def calculate_growth_streak_days(db: Session, student_id: int) -> int:
        rows = db.scalars(
            select(distinct(PointLog.created_at))
            .where(PointLog.student_id == student_id, PointLog.point_change > 0)
            .order_by(PointLog.created_at.desc())
        ).all()
        if not rows:
            return 0

        days = sorted({row.date() for row in rows}, reverse=True)
        streak = 1
        cursor = days[0]
        for current in days[1:]:
            if current == cursor - timedelta(days=1):
                streak += 1
                cursor = current
            else:
                break
        return streak

    @staticmethod
    def _build_unlock_conditions(db: Session, student: Student, student_pet: StudentPet) -> dict[str, bool]:
        streak = BadgeService.calculate_growth_streak_days(db, student.id)

        return {
            'stage_first_evolution': student_pet.stage_index >= 2,
            'stage_super_evolution': student_pet.stage_index >= 3,
            'stage_ultimate_evolution': student_pet.stage_index >= 4,
            'level_10': student_pet.level >= 10,
            'level_20': student_pet.level >= 20,
            'level_30': student_pet.level >= 30,
            'streak_3': streak >= 3,
            'streak_7': streak >= 7,
            'attr_wisdom_120': student_pet.wisdom >= 120,
            'attr_focus_120': student_pet.focus >= 120,
            'attr_affinity_120': student_pet.affinity >= 120,
            'attr_resilience_120': student_pet.resilience >= 120,
            'attr_vitality_120': student_pet.vitality >= 120,
        }

    @staticmethod
    def sync_badges(db: Session, student: Student, student_pet: StudentPet) -> list[StudentPetBadge]:
        badges = {badge.code: badge for badge in db.scalars(select(Badge)).all()}
        if not badges:
            return []

        existing = {
            item.badge.code: item
            for item in db.scalars(
                select(StudentPetBadge)
                .options(selectinload(StudentPetBadge.badge))
                .where(StudentPetBadge.student_pet_id == student_pet.id)
            ).all()
        }

        conditions = BadgeService._build_unlock_conditions(db, student, student_pet)
        unlocked: list[StudentPetBadge] = []

        for code, condition in conditions.items():
            if not condition:
                continue
            if code in existing:
                continue

            badge = badges.get(code)
            if not badge:
                continue

            record = StudentPetBadge(student_pet_id=student_pet.id, badge_id=badge.id)
            db.add(record)
            db.flush()
            unlocked.append(
                db.scalar(
                    select(StudentPetBadge)
                    .options(selectinload(StudentPetBadge.badge))
                    .where(StudentPetBadge.id == record.id)
                )
            )

        return unlocked

    @staticmethod
    def list_student_pet_badges(db: Session, student_pet_id: int) -> list[StudentPetBadge]:
        return list(
            db.scalars(
                select(StudentPetBadge)
                .options(selectinload(StudentPetBadge.badge))
                .where(StudentPetBadge.student_pet_id == student_pet_id)
                .order_by(StudentPetBadge.created_at.asc())
            ).all()
        )

    @staticmethod
    def to_badge_response(records: list[StudentPetBadge]) -> list[BadgeResponse]:
        return [
            BadgeResponse(
                id=item.badge.id,
                code=item.badge.code,
                name=item.badge.name,
                description=item.badge.description,
                rarity=item.badge.rarity,
                unlocked_at=item.created_at,
            )
            for item in records
        ]
