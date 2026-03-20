from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Badge(Base):
    __tablename__ = 'badges'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rarity: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    student_pet_badges = relationship('StudentPetBadge', back_populates='badge', cascade='all, delete-orphan')


class StudentPetBadge(Base):
    __tablename__ = 'student_pet_badges'
    __table_args__ = (UniqueConstraint('student_pet_id', 'badge_id', name='uq_student_pet_badge'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_pet_id: Mapped[int] = mapped_column(ForeignKey('student_pets.id', ondelete='CASCADE'), nullable=False)
    badge_id: Mapped[int] = mapped_column(ForeignKey('badges.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    student_pet = relationship('StudentPet', back_populates='badges')
    badge = relationship('Badge', back_populates='student_pet_badges')
