# Simple FastAPI CRUD API

A clean, industry-standard CRUD project using **FastAPI** and **SQLModel** (SQLite).

## Folder Structure

```
CRUD/
├── app/
│   ├── __init__.py
│   ├── database.py       # Database connection & session management
│   ├── models.py         # Database tables (SQLModel)
│   ├── schemas.py        # Request & response validation (Pydantic)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── items.py      # CRUD route handlers
│   └── main.py           # FastAPI entrypoint & lifespan
├── requirements.txt
└── README.md
```

## How to Run

1. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Run with FastAPI CLI:
   ```bash
   fastapi dev app/main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Open Swagger Interactive Docs:
   - URL: `http://localhost:8000/docs`
