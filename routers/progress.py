from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.goal import Goal
from models.progress import Progress
from models.user import User
from schemas.progress import ProgressCreate, ProgressResponse
from auth.dependencies import get_current_user

router = APIRouter(prefix="/goals/{goal_id}/progress", tags=["Progress"])


def _get_goal_or_404(goal_id: int, user_id: int, db: Session) -> Goal:
    """Helper: ambil goal dan validasi kepemilikan."""
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.owner_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Goal dengan ID {goal_id} tidak ditemukan")
    return goal


@router.post("/", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED,
             summary="Catat progress pada sebuah goal (perlu token)")
def add_progress(
    goal_id: int,
    progress_data: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Menambahkan log progress ke goal tertentu.
    Nilai current_value pada goal akan otomatis bertambah.
    Jika current_value >= target_value, status goal otomatis menjadi 'completed'.
    """
    goal = _get_goal_or_404(goal_id, current_user.id, db)

    log = Progress(
        value_added=progress_data.value_added,
        note=progress_data.note,
        goal_id=goal.id,
    )
    db.add(log)

    goal.current_value += progress_data.value_added

    # Auto-complete jika sudah mencapai target
    if goal.current_value >= goal.target_value and goal.status == "active":
        goal.current_value = goal.target_value  # cap agar tidak melebihi
        goal.status = "completed"

    db.commit()
    db.refresh(log)
    return log


@router.get("/", response_model=List[ProgressResponse],
            summary="Lihat semua progress log pada sebuah goal (perlu token)")
def get_progress_logs(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mengembalikan seluruh riwayat progress log dari goal tertentu."""
    _get_goal_or_404(goal_id, current_user.id, db)
    logs = db.query(Progress).filter(Progress.goal_id == goal_id)\
              .order_by(Progress.logged_at.desc()).all()
    return logs


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Hapus satu progress log (perlu token)")
def delete_progress_log(
    goal_id: int,
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Menghapus satu log progress. Nilai current_value goal akan dikurangi kembali."""
    goal = _get_goal_or_404(goal_id, current_user.id, db)

    log = db.query(Progress).filter(Progress.id == log_id, Progress.goal_id == goal_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Progress log dengan ID {log_id} tidak ditemukan")

    goal.current_value = max(0.0, goal.current_value - log.value_added)
    if goal.status == "completed" and goal.current_value < goal.target_value:
        goal.status = "active"

    db.delete(log)
    db.commit()
