from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class GoalStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    paused = "paused"
    cancelled = "cancelled"


class GoalCategory(str, enum.Enum):
    health = "health"
    education = "education"
    finance = "finance"
    career = "career"
    personal = "personal"
    other = "other"


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default=GoalCategory.personal)
    status = Column(String(20), default=GoalStatus.active)
    target_value = Column(Float, default=100.0)   # nilai target (misal: 100 km, 100%)
    current_value = Column(Float, default=0.0)     # nilai sekarang
    unit = Column(String(30), default="%")         # satuan (km, %, buku, dsb.)
    deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign Key ke User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relasi balik ke User
    owner = relationship("User", back_populates="goals")

    # Relasi One-to-Many: satu goal memiliki banyak progress log
    progress_logs = relationship("Progress", back_populates="goal", cascade="all, delete-orphan")
