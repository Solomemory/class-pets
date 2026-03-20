from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.models.badge import StudentPetBadge
from app.models.pet import PetStageConfig, PetTemplate, StudentPet
from app.models.point_log import PointLog
from app.models.student import Student
from app.schemas.pet import (
    PetAttributeResponse,
    PetStageConfigResponse,
    StudentPetStatusResponse,
)
from app.services.badge_service import BadgeService


@dataclass(frozen=True)
class StageRule:
    stage_index: int
    label: str
    level_min: int
    level_max: int | None


@dataclass(frozen=True)
class RouteMeta:
    key: str
    label: str
    theme: str


class GrowthService:
    STAGE_RULES = [
        StageRule(stage_index=1, label='初始形态', level_min=1, level_max=9),
        StageRule(stage_index=2, label='进化形态', level_min=10, level_max=19),
        StageRule(stage_index=3, label='超进化形态', level_min=20, level_max=99),
        StageRule(stage_index=4, label='究极进化形态', level_min=100, level_max=None),
    ]

    ATTRIBUTE_LABELS = {
        'wisdom': '智慧',
        'focus': '专注',
        'affinity': '亲和',
        'resilience': '毅力',
        'vitality': '活力',
    }

    REASON_ATTRIBUTE_WEIGHTS = {
        '回答问题': {'wisdom': 2, 'focus': 1},
        '完成作业': {'resilience': 2},
        '课堂纪律优秀': {'focus': 2},
        '小组协作': {'affinity': 2},
        '课堂挑战完成': {'vitality': 2, 'resilience': 1},
    }

    DEFAULT_REASON_WEIGHTS = {'focus': 1}

    ROUTE_BY_ATTRIBUTE = {
        'wisdom': RouteMeta(key='starlight', label='星辉', theme='#79c7ff'),
        'vitality': RouteMeta(key='blaze', label='焰痕', theme='#ff9561'),
        'focus': RouteMeta(key='frost', label='霜界', theme='#9ed8ff'),
        'affinity': RouteMeta(key='sanctuary', label='圣域', theme='#8ff0cb'),
        'resilience': RouteMeta(key='ironcore', label='玄铠', theme='#c2b8a6'),
    }

    ATTRIBUTE_PRIORITY = ['wisdom', 'vitality', 'focus', 'affinity', 'resilience']

    TITLE_SUFFIX_BY_ROUTE = {
        'starlight': '执律者',
        'blaze': '征服者',
        'frost': '守望者',
        'sanctuary': '共鸣体',
        'ironcore': '誓约灵',
    }

    STATUS_LABELS = {
        'stable': '平稳',
        'growing': '成长中',
        'energized': '高能',
        'glorious': '荣耀',
        'peak': '巅峰',
        'resting': '恢复中',
    }

    @classmethod
    def calculate_level(cls, total_points: int) -> int:
        return max(1, (total_points // settings.points_per_level) + 1)

    @classmethod
    def calculate_stage_index(cls, level: int) -> int:
        for rule in cls.STAGE_RULES:
            if rule.level_max is None and level >= rule.level_min:
                return rule.stage_index
            if rule.level_max is not None and rule.level_min <= level <= rule.level_max:
                return rule.stage_index
        return 1

    @classmethod
    def calculate_stage_star(cls, level: int, stage_index: int) -> int:
        rule = cls.get_stage_rule(stage_index)
        if rule.level_max is None:
            # 究极阶段采用每 10 级一档，最多 3 星。
            return min(3, ((level - rule.level_min) // 10) + 1)

        span = rule.level_max - rule.level_min + 1
        segment = max(1, (span + 2) // 3)
        offset = level - rule.level_min
        return min(3, (offset // segment) + 1)

    @classmethod
    def get_stage_rule(cls, stage_index: int) -> StageRule:
        return next(rule for rule in cls.STAGE_RULES if rule.stage_index == stage_index)

    @classmethod
    def get_next_stage_level(cls, stage_index: int) -> int | None:
        next_index = stage_index + 1
        for rule in cls.STAGE_RULES:
            if rule.stage_index == next_index:
                return rule.level_min
        return None

    @classmethod
    def calc_points_to_next_level(cls, total_points: int) -> int:
        remainder = total_points % settings.points_per_level
        return settings.points_per_level if remainder == 0 else settings.points_per_level - remainder

    @classmethod
    def calc_points_to_next_stage(cls, total_points: int, stage_index: int) -> int:
        next_stage_level = cls.get_next_stage_level(stage_index)
        if next_stage_level is None:
            return 0
        required_points = (next_stage_level - 1) * settings.points_per_level
        return max(0, required_points - total_points)

    @classmethod
    def calculate_attribute_delta(cls, reason: str, point_change: int) -> dict[str, int]:
        if point_change == 0:
            return {key: 0 for key in cls.ATTRIBUTE_LABELS}

        weights = cls.REASON_ATTRIBUTE_WEIGHTS.get(reason, cls.DEFAULT_REASON_WEIGHTS)
        units = max(1, abs(point_change) // 20)
        sign = 1 if point_change > 0 else -1

        result = {key: 0 for key in cls.ATTRIBUTE_LABELS}
        for key, weight in weights.items():
            result[key] = sign * units * weight
        return result

    @classmethod
    def apply_attribute_delta(cls, student_pet: StudentPet, delta: dict[str, int]) -> None:
        student_pet.wisdom = max(0, student_pet.wisdom + delta.get('wisdom', 0))
        student_pet.focus = max(0, student_pet.focus + delta.get('focus', 0))
        student_pet.affinity = max(0, student_pet.affinity + delta.get('affinity', 0))
        student_pet.resilience = max(0, student_pet.resilience + delta.get('resilience', 0))
        student_pet.vitality = max(0, student_pet.vitality + delta.get('vitality', 0))

    @classmethod
    def _build_stage_preview(cls, stage_configs: list[PetStageConfig]) -> list[PetStageConfigResponse]:
        ordered = sorted(stage_configs, key=lambda s: s.stage_index)
        return [PetStageConfigResponse.model_validate(item) for item in ordered]

    @classmethod
    def _determine_dominant_attribute(cls, student_pet: StudentPet) -> tuple[str, int]:
        attr_values = {
            'wisdom': student_pet.wisdom,
            'focus': student_pet.focus,
            'affinity': student_pet.affinity,
            'resilience': student_pet.resilience,
            'vitality': student_pet.vitality,
        }
        max_value = max(attr_values.values())
        for key in cls.ATTRIBUTE_PRIORITY:
            if attr_values[key] == max_value:
                return key, max_value
        return 'wisdom', attr_values['wisdom']

    @classmethod
    def determine_route(cls, student_pet: StudentPet) -> tuple[RouteMeta, str, str]:
        dominant_key, _ = cls._determine_dominant_attribute(student_pet)
        route = cls.ROUTE_BY_ATTRIBUTE[dominant_key]
        return route, dominant_key, cls.ATTRIBUTE_LABELS[dominant_key]

    @classmethod
    def determine_title(cls, route_key: str) -> str:
        route = next((item for item in cls.ROUTE_BY_ATTRIBUTE.values() if item.key == route_key), None)
        suffix = cls.TITLE_SUFFIX_BY_ROUTE.get(route_key, '守望者')
        if not route:
            return f'星辉{suffix}'
        return f'{route.label}{suffix}'

    @classmethod
    def _recent_points_sum(cls, db: Session, student_id: int, days: int = 7) -> int:
        since_time = datetime.utcnow() - timedelta(days=days)
        points = db.scalar(
            select(func.coalesce(func.sum(PointLog.point_change), 0)).where(
                PointLog.student_id == student_id,
                PointLog.created_at >= since_time,
            )
        )
        return int(points or 0)

    @classmethod
    def determine_status(cls, db: Session, student: Student, student_pet: StudentPet, badge_count: int) -> str:
        recent_points = cls._recent_points_sum(db, student.id, days=7)
        streak_days = BadgeService.calculate_growth_streak_days(db, student.id)

        if student_pet.stage_index >= 4 and student_pet.stage_star >= 3:
            return 'peak'
        if badge_count >= 6 or student_pet.stage_index >= 4:
            return 'glorious'
        if recent_points >= 300:
            return 'energized'
        if streak_days >= 2:
            return 'growing'
        if recent_points <= 0 and student_pet.level >= 10:
            return 'resting'
        return 'stable'

    @classmethod
    def refresh_meta_fields(cls, db: Session, student: Student, student_pet: StudentPet, badge_count: int) -> None:
        route, _, _ = cls.determine_route(student_pet)
        student_pet.growth_route = route.key
        student_pet.growth_title = cls.determine_title(route.key)
        student_pet.current_status = cls.determine_status(db, student, student_pet, badge_count)

    @classmethod
    def recalculate_student_pet(cls, db: Session, student: Student) -> StudentPet | None:
        student_pet = db.scalar(
            select(StudentPet)
            .options(
                selectinload(StudentPet.pet_template).selectinload(PetTemplate.stage_configs),
                selectinload(StudentPet.badges).selectinload(StudentPetBadge.badge),
            )
            .where(StudentPet.student_id == student.id)
        )
        if not student_pet:
            return None

        now = datetime.utcnow()
        old_stage_index = student_pet.stage_index
        old_level = student_pet.level

        level = cls.calculate_level(student.total_points)
        stage_index = cls.calculate_stage_index(level)
        stage_star = cls.calculate_stage_star(level, stage_index)

        stage_config = next(
            (cfg for cfg in student_pet.pet_template.stage_configs if cfg.stage_index == stage_index),
            None,
        )
        if stage_config is None:
            raise ValueError(f'宠物模板 {student_pet.pet_template_id} 缺少阶段 {stage_index} 配置')

        student_pet.level = level
        student_pet.stage_index = stage_index
        student_pet.stage_star = stage_star
        student_pet.current_stage_name = stage_config.stage_name
        student_pet.current_stage_description = stage_config.stage_description
        student_pet.current_image_prompt = stage_config.image_prompt
        student_pet.points_to_next_level = cls.calc_points_to_next_level(student.total_points)
        student_pet.points_to_next_stage = cls.calc_points_to_next_stage(student.total_points, stage_index)
        student_pet.next_stage_level = cls.get_next_stage_level(stage_index)

        if old_level <= 1 and level > 1 and student_pet.first_level_up_at is None:
            student_pet.first_level_up_at = now
        if old_stage_index < 2 and stage_index >= 2 and student_pet.first_evolution_at is None:
            student_pet.first_evolution_at = now
        if old_stage_index < 3 and stage_index >= 3 and student_pet.first_super_evolution_at is None:
            student_pet.first_super_evolution_at = now
        if old_stage_index < 4 and stage_index >= 4 and student_pet.ultimate_evolution_at is None:
            student_pet.ultimate_evolution_at = now

        badge_count = len(student_pet.badges)
        cls.refresh_meta_fields(db, student, student_pet, badge_count)

        db.add(student_pet)
        db.flush()
        student_pet._evolution_switched = old_stage_index != stage_index  # type: ignore[attr-defined]
        return student_pet

    @classmethod
    def build_attribute_snapshot(cls, student_pet: StudentPet) -> PetAttributeResponse:
        route, dominant_key, dominant_label = cls.determine_route(student_pet)
        return PetAttributeResponse(
            wisdom=student_pet.wisdom,
            focus=student_pet.focus,
            affinity=student_pet.affinity,
            resilience=student_pet.resilience,
            vitality=student_pet.vitality,
            dominant_attribute_key=dominant_key,
            dominant_attribute_label=dominant_label,
        )

    @classmethod
    def build_status_dto(
        cls,
        student: Student,
        student_pet: StudentPet,
        db: Session | None = None,
        badge_records: list[StudentPetBadge] | None = None,
    ) -> StudentPetStatusResponse:
        stage_preview = cls._build_stage_preview(student_pet.pet_template.stage_configs)
        stage_rule = cls.get_stage_rule(student_pet.stage_index)
        evolution_switched = getattr(student_pet, '_evolution_switched', False)

        if badge_records is not None:
            badge_count = len(badge_records)
        else:
            badge_count = len(getattr(student_pet, 'badges', []) or [])

        route, _, _ = cls.determine_route(student_pet)
        status_key = student_pet.current_status
        if db:
            status_key = cls.determine_status(db, student, student_pet, badge_count)

        return StudentPetStatusResponse(
            student_pet_id=student_pet.id,
            pet_template_id=student_pet.pet_template_id,
            pet_name=student_pet.pet_template.name,
            pet_type=student_pet.pet_template.pet_type,
            rarity=student_pet.pet_template.rarity,
            total_points=student.total_points,
            level=student_pet.level,
            stage_index=student_pet.stage_index,
            stage_label=stage_rule.label,
            stage_star=student_pet.stage_star,
            stage_star_label=f'{student_pet.stage_star}星成长',
            route_key=route.key,
            route_label=route.label,
            route_theme=route.theme,
            title=cls.determine_title(route.key),
            status_key=status_key,
            status_label=cls.STATUS_LABELS.get(status_key, '平稳'),
            current_stage_name=student_pet.current_stage_name,
            current_stage_description=student_pet.current_stage_description,
            current_image_prompt=student_pet.current_image_prompt,
            points_per_level=settings.points_per_level,
            points_to_next_level=student_pet.points_to_next_level,
            points_to_next_stage=student_pet.points_to_next_stage,
            next_stage_level=student_pet.next_stage_level,
            evolution_switched=evolution_switched,
            attributes=cls.build_attribute_snapshot(student_pet),
            unlocked_badge_count=badge_count,
            stage_preview=stage_preview,
        )

    @classmethod
    def get_rule_payload(cls) -> list[dict[str, int | str | None]]:
        return [
            {
                'stage_index': rule.stage_index,
                'stage_label': rule.label,
                'level_min': rule.level_min,
                'level_max': rule.level_max,
            }
            for rule in cls.STAGE_RULES
        ]
