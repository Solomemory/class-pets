from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    grade_class: Mapped[str | None] = mapped_column(String(50), nullable=True)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    pet = relationship('StudentPet', back_populates='student', uselist=False, cascade='all, delete-orphan')
    point_logs = relationship('PointLog', back_populates='student', cascade='all, delete-orphan')
