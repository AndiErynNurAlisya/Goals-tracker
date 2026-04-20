from sqlalchemy import Column, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Progress(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    value_added = Column(Float, nullable=False)         # nilai yang ditambahkan pada sesi ini
    note = Column(Text, nullable=True)                  # catatan opsional
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign Key ke Goal
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)

    # Relasi balik ke Goal
    goal = relationship("Goal", back_populates="progress_logs")
