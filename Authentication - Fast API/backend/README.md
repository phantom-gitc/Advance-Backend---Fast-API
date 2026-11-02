# FastAPI Authentication & User Management System

A simple, secure, and beginner-friendly authentication system built with **FastAPI**, **MongoDB**, and **JWT**.

---

## Features

- **Secure Password Hashing:** Uses bcrypt with automatic salting.
- **JWT Authentication:** Short-lived access tokens (15 mins) and long-lived refresh tokens (7 days).
- **HTTP-Only Cookies:** Tokens stored securely in cookies to prevent XSS attacks.
- **Refresh Token Rotation:** Every refresh creates a new token and revokes the old one.
- **Token Reuse Detection:** Reusing a revoked token invalidates all user sessions for safety.
- **Role-Based Access Control (RBAC):** Two roles (`user` and `admin`).
- **Rate Limiting:** Protects `/register`, `/login`, and `/refresh-token` against brute force using SlowAPI.
- **Complete User CRUD:** Users can view, update, and delete their own profile. Admins can view, update, and delete any user.

---

## Folder Structure

```
backend/
├── app/
│   ├── main.py              # App entry point, CORS, and routers
│   ├── config.py            # Central settings from .env
│   ├── database.py          # MongoDB async connection & indexes
│   ├── limiter.py           # SlowAPI rate limiter
│   ├── models/
│   │   └── user_model.py    # Document serializer helper
│   ├── schemas/
│   │   ├── auth_schema.py   # Register, login, and response schemas
│   │   └── user_schema.py   # User update schemas
│   ├── routes/
│   │   ├── auth_routes.py   # Auth endpoints
│   │   └── user_routes.py   # User management endpoints
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   └── user_controller.py
│   ├── middleware/
│   │   └── auth_middleware.py # get_current_user and get_admin_user
│   ├── services/
│   │   └── auth_service.py    # Business logic & database operations
│   └── utils/
│       ├── password.py        # bcrypt hashing and verification
│       ├── jwt.py             # JWT generation and verification
│       └── cookies.py         # HTTP-only cookie helpers
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Prerequisites
- Python 3.11+
- MongoDB installed and running locally on port 27017 (or MongoDB Atlas)

### 2. Create Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

To generate strong random JWT secrets in Python:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Paste the generated strings into `ACCESS_TOKEN_SECRET` and `REFRESH_TOKEN_SECRET` in your `.env` file.

---

## Running the Application

From inside the `backend` folder:
```bash
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`  
Interactive Swagger API documentation: `http://localhost:8000/docs`

---

## API Endpoints

### Authentication (`/api/auth`)
| Method | Endpoint | Description | Rate Limit |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register new user | 5/min |
| `POST` | `/api/auth/login` | Login and set HTTP-only cookies | 5/min |
| `POST` | `/api/auth/refresh-token` | Rotate refresh token | 10/min |
| `POST` | `/api/auth/logout` | Logout and clear cookies | None |
| `GET` | `/api/auth/me` | Get currently logged-in user profile | None |

### User Management (`/api/users`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/users/me` | Get own profile | User / Admin |
| `PATCH` | `/api/users/me` | Update full name | User / Admin |
| `DELETE` | `/api/users/me` | Delete own account and sessions | User / Admin |
| `GET` | `/api/users/` | Paginated user list (`?page=1&limit=10`) | Admin only |
| `GET` | `/api/users/{user_id}` | Get specific user | Admin only |
| `PATCH` | `/api/users/{user_id}` | Update user role or status | Admin only |
| `DELETE` | `/api/users/{user_id}` | Delete user account and sessions | Admin only |
| `GET` | `/health` | Health check | Public |

