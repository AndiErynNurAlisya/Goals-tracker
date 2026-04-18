from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.goal import GoalStatus, GoalCategory


# Schema untuk membuat goal
class GoalCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150, examples=["Lari 100 km bulan ini"])
    description: Optional[str] = Field(None, examples=["Target lari pagi setiap hari"])
    category: GoalCategory = Field(default=GoalCategory.personal)
    target_value: float = Field(default=100.0, gt=0, examples=[100.0])
    unit: str = Field(default="%", max_length=30, examples=["km"])
    deadline: Optional[datetime] = Field(None, examples=["2025-12-31T00:00:00"])


# Schema untuk update goal (semua field opsional)
class GoalUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = None
    category: Optional[GoalCategory] = None
    status: Optional[GoalStatus] = None
    target_value: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = Field(None, max_length=30)
    deadline: Optional[datetime] = None


# Schema summary progress dalam response goal
class ProgressSummary(BaseModel):
    id: int
    value_added: float
    note: Optional[str]
    logged_at: datetime

    model_config = {"from_attributes": True}


# Schema response goal
class GoalResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str
    status: str
    target_value: float
    current_value: float
    unit: str
    deadline: Optional[datetime]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    progress_logs: List[ProgressSummary] = []

    model_config = {"from_attributes": True}


# Schema ringkas (tanpa progress logs) untuk list endpoint
class GoalShort(BaseModel):
    id: int
    title: str
    category: str
    status: str
    current_value: float
    target_value: float
    unit: str
    deadline: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}
