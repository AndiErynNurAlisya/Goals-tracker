from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema untuk menambah progress
class ProgressCreate(BaseModel):
    value_added: float = Field(..., gt=0, examples=[5.0])
    note: Optional[str] = Field(None, examples=["Lari pagi 5 km"])


# Schema response progress
class ProgressResponse(BaseModel):
    id: int
    value_added: float
    note: Optional[str]
    logged_at: datetime
    goal_id: int

    model_config = {"from_attributes": True}
