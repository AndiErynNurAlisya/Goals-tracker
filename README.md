# Goals Tracker API

Proyek UTS Pemrograman Web Lanjutan — Microservice RESTful API menggunakan FastAPI.

## Deskripsi

Goals Tracker adalah sistem manajemen target pribadi di mana setiap user dapat membuat, memantau, dan menyelesaikan goal yang mereka miliki. Setiap goal memiliki riwayat progress yang dicatat secara bertahap.

## Stack Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Framework | FastAPI |
| Bahasa | Python 3.9+ |
| ORM | SQLAlchemy + PyMySQL |
| Database | MySQL |
| Autentikasi | JWT (python-jose) |
| Hashing | bcrypt (passlib) |
| Deployment | Uvicorn (localhost) |
| Testing | Postman |

## Struktur Proyek

```
goals_tracker/
├── main.py           # Entry point FastAPI
├── database.py       # Koneksi & session database
├── requirements.txt  # Dependensi Python
├── README.md         # Dokumentasi ini
├── models/
│   ├── user.py       # Model User
│   ├── goal.py       # Model Goal (beserta enum status & kategori)
│   └── progress.py   # Model Progress log
├── schemas/
│   ├── user.py       # Pydantic schema User
│   ├── goal.py       # Pydantic schema Goal
│   └── progress.py   # Pydantic schema Progress
├── routers/
│   ├── users.py      # Endpoint /users (register, login, me)
│   ├── goals.py      # Endpoint /goals (CRUD)
│   └── progress.py   # Endpoint /goals/{id}/progress
└── auth/
    ├── jwt_handler.py    # Buat & verifikasi JWT
    └── dependencies.py   # Dependency get_current_user
```

## Cara Menjalankan

```bash
# 1. Clone / extract proyek
cd goals_tracker

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Buka dokumentasi Swagger UI
# http://localhost:8000/docs
```

## Endpoint API

### Users
| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| POST | /users/register | ❌ | Daftar user baru |
| POST | /users/login | ❌ | Login → dapat JWT token |
| GET | /users/me | ✅ | Lihat profil sendiri |

### Goals
| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| POST | /goals/ | ✅ | Buat goal baru |
| GET | /goals/ | ✅ | Lihat semua goal saya |
| GET | /goals/{id} | ✅ | Detail goal + progress log |
| PUT | /goals/{id} | ✅ | Update goal |
| DELETE | /goals/{id} | ✅ | Hapus goal |

### Progress
| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| POST | /goals/{id}/progress/ | ✅ | Catat progress |
| GET | /goals/{id}/progress/ | ✅ | Lihat semua progress log |
| DELETE | /goals/{id}/progress/{log_id} | ✅ | Hapus progress log |

## Relasi Database (ERD)

```
users (1) ──────< goals (Many)
                    │
                    └──────< progress_logs (Many)
```

- Satu **User** memiliki banyak **Goal** (One-to-Many)
- Satu **Goal** memiliki banyak **Progress Log** (One-to-Many)

## Cara Autentikasi di Swagger UI

1. Jalankan `POST /users/register` untuk daftar
2. Jalankan `POST /users/login` → salin `access_token`
3. Klik tombol **Authorize 🔒** di kanan atas Swagger UI
4. Isi `Value: <token_anda>` → klik Authorize
5. Semua endpoint bertanda 🔒 kini dapat diakses

## Konfigurasi MySQL

Buat database terlebih dahulu di MySQL:

```sql
CREATE DATABASE goals_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Lalu sesuaikan variabel di `database.py` (atau gunakan environment variable):

```bash
# Opsi 1: Edit langsung di database.py
DB_USER     = "root"
DB_PASSWORD = "password_mysql_kamu"
DB_NAME     = "goals_tracker"

# Opsi 2: Pakai environment variable saat menjalankan
DB_USER=root DB_PASSWORD=secret uvicorn main:app --reload
```
