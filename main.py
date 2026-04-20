from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models import user, goal, progress  

from routers import users, goals, progress as progress_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Goals Tracker API",
    description="""
## Goals Tracker — RESTful API

Sistem manajemen target pribadi berbasis microservice.

### Fitur Utama
- **User Management** : Register & login dengan JWT authentication
- **Goal CRUD** : Buat, lihat, update, dan hapus goal pribadi
- **Progress Tracking** : Catat kemajuan setiap goal secara bertahap
- **Auto-Complete** : Goal otomatis selesai saat target tercapai

### Cara Menggunakan
1. **Register** di `/users/register`
2. **Login** di `/users/login` → salin `access_token`
3. Klik tombol **Authorize** di atas → masukkan token
4. Akses semua endpoint yang membutuhkan autentikasi
    """,
    version="1.0.0",
    contact={
        "name": "Goals Tracker",
    },
)

# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(users.router)
app.include_router(goals.router)
app.include_router(progress_router.router)


# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Selamat datang di Goals Tracker API ",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Endpoint untuk mengecek status server."""
    return {"status": "ok", "service": "goals-tracker"}
