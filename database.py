from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

# ── Konfigurasi koneksi MySQL ─────────────────────────────────────────────────
# Ganti nilai di bawah sesuai konfigurasi MySQL lokal kamu
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "goals_tracker")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=False,          # Set True untuk debug query SQL di terminal
    pool_pre_ping=True,  # Cek koneksi sebelum dipakai (penting untuk MySQL)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dependency untuk mendapatkan DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
