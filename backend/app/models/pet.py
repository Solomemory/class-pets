from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PetTemplate(Base):
    __tablename__ = 'pet_templates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    pet_type: Mapped[str] = mapped_column(String(50), nullable=False)
    lore: Mapped[str] = mapped_column(Text, nullable=False)
    rarity: Mapped[str] = mapped_column(String(20), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    stage_configs = relationship('PetStageConfig', back_populates='pet_template', cascade='all, delete-orphan')
    student_pets = relationship('StudentPet', back_populates='pet_template')


class PetStageConfig(Base):
    __tablename__ = 'pet_stage_configs'
    __table_args__ = (UniqueConstraint('pet_template_id', 'stage_index', name='uq_pet_stage'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_template_id: Mapped[int] = mapped_column(ForeignKey('pet_templates.id', ondelete='CASCADE'), nullable=False)
    stage_index: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_key: Mapped[str] = mapped_column(String(30), nullable=False)
    stage_name: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_description: Mapped[str] = mapped_column(Text, nullable=False)
    image_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    level_min: Mapped[int] = mapped_column(Integer, nullable=False)
    level_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    pet_template = relationship('PetTemplate', back_populates='stage_configs')


class StudentPet(Base):
    __tablename__ = 'student_pets'
    __table_args__ = (UniqueConstraint('student_id', name='uq_student_main_pet'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    pet_template_id: Mapped[int] = mapped_column(ForeignKey('pet_templates.id', ondelete='RESTRICT'), nullable=False)

    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    stage_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    stage_star: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    wisdom: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    focus: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    affinity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    resilience: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    vitality: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    growth_route: Mapped[str] = mapped_column(String(30), nullable=False, default='starlight')
    growth_title: Mapped[str] = mapped_column(String(100), nullable=False, default='星辉执律者')
    current_status: Mapped[str] = mapped_column(String(30), nullable=False, default='stable')

    current_stage_name: Mapped[str] = mapped_column(String(100), nullable=False)
    current_stage_description: Mapped[str] = mapped_column(Text, nullable=False)
    current_image_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    points_to_next_level: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    points_to_next_stage: Mapped[int] = mapped_column(Integer, nullable=False, default=900)
    next_stage_level: Mapped[int | None] = mapped_column(Integer, nullable=True)

    first_level_up_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    first_evolution_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    first_super_evolution_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ultimate_evolution_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    student = relationship('Student', back_populates='pet')
    pet_template = relationship('PetTemplate', back_populates='student_pets')
    badges = relationship('StudentPetBadge', back_populates='student_pet', cascade='all, delete-orphan')
