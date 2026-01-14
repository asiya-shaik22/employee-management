# Employee Management API

## Overview
A simple REST API built using FastAPI to manage employees in a company.
The API supports CRUD operations, JWT-based authentication, filtering,
pagination, and proper error handling.

---

## Tech Stack
- Python
- FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy
- JWT Authentication
- Pytest

---

## Setup

### 1. Create virtual environment
```bash
python -m venv .venv
```

Activate:
```bash
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # Linux / Mac
```

---

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

### 3. Environment variables
Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:<PASSWORD>@db.<PROJECT_ID>.supabase.co:5432/postgres
JWT_SECRET_KEY=supersecretkey
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 4. Run the application
```bash
uvicorn app.main:app --reload
```

Swagger UI:
http://127.0.0.1:8000/docs

---

## Authentication

### Get Token
```
POST /api/token
```

Credentials:
```
username: admin
password: admin123
```

Use the returned token as **Bearer Token** for all employee APIs.

---

## API Endpoints

### Employees
- `POST /api/employees/` → Create employee (201)
- `GET /api/employees/` → List employees (pagination + filters)
- `GET /api/employees/{id}` → Get employee by ID
- `PUT /api/employees/{id}` → Update employee
- `DELETE /api/employees/{id}` → Delete employee (204)

---

## Status Codes
- 201 Created
- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 204 No Content

---

## Testing

Run tests:
```bash
pytest -v
```

Tests cover:
- Authentication
- Employee CRUD (happy paths)
- Validation and error cases

---

## Summary
This project demonstrates RESTful API design, authentication,
validation, error handling, and basic testing using FastAPI.
