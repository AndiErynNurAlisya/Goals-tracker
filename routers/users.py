from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, UserLogin, Token
from auth.jwt_handler import create_access_token
from auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="Daftarkan user baru")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Mendaftarkan user baru ke sistem."""
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username sudah digunakan")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email sudah digunakan")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token, summary="Login dan dapatkan JWT token")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login dengan username & password, mengembalikan JWT access token."""
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse, summary="Lihat profil user saat ini (perlu token)")
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Endpoint terproteksi: mengembalikan data profil user yang sedang login."""
    return current_user
