from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.goal import Goal, GoalStatus
from models.user import User
from schemas.goal import GoalCreate, GoalUpdate, GoalResponse, GoalShort
from auth.dependencies import get_current_user

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED,
             summary="Buat goal baru (perlu token)")
def create_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Membuat goal baru untuk user yang sedang login."""
    new_goal = Goal(
        title=goal_data.title,
        description=goal_data.description,
        category=goal_data.category.value,
        target_value=goal_data.target_value,
        unit=goal_data.unit,
        deadline=goal_data.deadline,
        owner_id=current_user.id,
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal


@router.get("/", response_model=List[GoalShort], summary="Lihat semua goal milik saya (perlu token)")
def get_my_goals(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter berdasarkan status: active, completed, paused, cancelled"),
    category: Optional[str] = Query(None, description="Filter berdasarkan kategori"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mengembalikan semua goal milik user yang sedang login, dengan filter opsional."""
    query = db.query(Goal).filter(Goal.owner_id == current_user.id)
    if status_filter:
        query = query.filter(Goal.status == status_filter)
    if category:
        query = query.filter(Goal.category == category)
    return query.order_by(Goal.created_at.desc()).all()


@router.get("/{goal_id}", response_model=GoalResponse, summary="Lihat detail goal (perlu token)")
def get_goal_detail(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mengembalikan detail goal beserta seluruh progress log-nya."""
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.owner_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Goal dengan ID {goal_id} tidak ditemukan")
    return goal


@router.put("/{goal_id}", response_model=GoalResponse, summary="Update goal (perlu token)")
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Memperbarui data goal. Hanya field yang dikirim yang akan diubah."""
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.owner_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Goal dengan ID {goal_id} tidak ditemukan")

    update_data = goal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(value, 'value'):
            value = value.value
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Hapus goal (perlu token)")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Menghapus goal beserta semua progress log-nya (cascade delete)."""
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.owner_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Goal dengan ID {goal_id} tidak ditemukan")
    db.delete(goal)
    db.commit()
