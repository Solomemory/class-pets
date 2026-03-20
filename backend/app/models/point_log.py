from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PointLog(Base):
    __tablename__ = 'point_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True)
    point_change: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(50), nullable=False)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)

    wisdom_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    focus_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    affinity_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    resilience_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    vitality_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    student = relationship('Student', back_populates='point_logs')
