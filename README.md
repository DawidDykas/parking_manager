# Parking Manager

Backend system for managing vehicle entry and exit events in a parking lot using license plate recognition.

The project provides an asynchronous REST API (FastAPI), performs plate detection in the background (Celery) with Redis as the broker, stores drive and user data (SQLAlchemy + SQL database), and handles JWT-based authorization.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Environment Configuration](#environment-configuration)
- [Run Locally](#run-locally)
- [Database Migrations](#database-migrations)
- [API Usage](#api-usage)
- [Example Workflow](#example-workflow)
- [Test Notebook](#test-notebook)
- [Logging and Security](#logging-and-security)
- [Roadmap / Possible Improvements](#roadmap--possible-improvements)
- [License](#license)

## Features

- User registration and login, plus a complete user management flow.
- JWT-protected endpoints (`Authorization: Bearer <token>`).
- Image upload to `driveIn` / `driveOut` endpoints.
- Asynchronous license plate processing via Celery.
- Storage and updates of drive history (`drive_in`, `drive_out`, `payment`).
- Drive filtering by ID, plate number, and date range.

## Architecture

High-level flow:

1. A client sends a plate image to a FastAPI endpoint (`/drives/driveIn/` or `/drives/driveOut/`).
2. The API queues the task in Celery and immediately returns a `task_id`.
3. A Celery worker runs the detection pipeline (YOLO + OCR).
4. Service-layer business logic validates parking rules and creates/updates the DB record.

## Tech Stack

### Backend API

- **FastAPI** (asynchronous) – modern REST API framework with typing support and automatic OpenAPI documentation.
- **Pydantic** – input/output validation and request/response schemas.

### Database and Migrations

- **SQLAlchemy (Async)** – asynchronous ORM layer and database sessions.
- **Alembic** – schema versioning and database migrations.
- **aiosqlite / SQL backend via URL** – the project reads `url_database` from environment settings.

### Async Tasks and Queue

- **Celery** – runs heavier operations (OCR detection) outside the API request/response cycle.
- **Redis** – queue broker for Celery.

### AI / Computer Vision

- **Ultralytics YOLO** – detects license plates in images.
- **EasyOCR** – recognizes characters from cropped plate regions.
- **OpenCV + NumPy + PIL** – image preprocessing and transformations.

### Security

- **PyJWT** – JWT token creation and validation.
- **Passlib (Argon2)** – password hashing and verification.

### Utility Tooling

- **Uvicorn** – ASGI server for FastAPI.
- **httpx** – asynchronous HTTP client (including testing scenarios).
- **Ruff / Black** – linting and code formatting.

## Project Structure

```text
app/
	api/
		routers/       # FastAPI endpoints (users, drives)
		services/      # business logic
		repositories/  # database operations
		schemas/       # Pydantic models
		modules/       # DB session, ORM tables
		security/      # JWT, password hashing
		utils/         # auth dependencies, etc.
	celery/
		setting_celery.py
		celery_drive.py
	models/
		prediction.py  # YOLO + OCR pipeline
		best.pt        # detection model weights
config/
	setting.py       # loads configuration from .env
migrations/
	versions/        # Alembic migration files
```

## Requirements

- Python 3.13+
- Redis
- Dependencies installed from `pyproject.toml`

## Environment Configuration

The application uses an `.env` file located at `config/.env`.

Create `config/.env` with a minimal setup:

```env
url_database=sqlite+aiosqlite:///./parking.db
SECRET_KEY=super-secret-key-change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
URL_BROKER=redis://localhost:6379/0
```

> You can replace `url_database` with PostgreSQL/MySQL (using SQLAlchemy async URL syntax).

## Run Locally

### 1) Install dependencies

Using `uv`:

```bash
uv sync
```

Or the classic approach:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Start the application

```bash
python -m app.api.main
```

After startup, API docs are available at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Database Migrations

An initial migration of the Alembic database was implemented, creating the database with the first user. 
This allowed for the database to be expanded based on project needs.

## API Usage

### User Endpoints (`/users`)

- `POST /users/create/` – create a new user.
- `POST /users/login/` – log in and return a JWT token (string).
- `POST /users/refresh` – refresh the token.
- `GET /users/by-id/{id}` – fetch user by ID (JWT required).
- `GET /users/by-email?email=...` – fetch user by email (JWT required).
- `POST /users/update` – update user data (JWT required).

### Drive Endpoints (`/drives`)

- `POST /drives/driveIn/` – upload image for entry detection.
- `POST /drives/driveOut/` – upload image for exit detection.
- `GET /drives/getDriveById/{drive_id}` – fetch drive record by ID (JWT).
- `PUT /drives/updateDrive/{drive_id}` – update a drive record (JWT).
- `DELETE /drives/deleteDrive/{drive_id}` – delete a drive record (JWT).
- `GET /drives/getDrivesByPlate/{plate}` – fetch history by plate number (JWT).
- `GET /drives/getDrivesByDateRange/?start_date=...&end_date=...` – filter by date range (JWT).

### Request Authorization

After login, include this header:

```http
Authorization: Bearer <jwt_token>
```

## Example Workflow

1. Create a user (`/users/create/`).
2. Log in (`/users/login/`) and get a token.
3. Send an image to `/drives/driveIn/`.
4. After payment, update the record (`/drives/updateDrive/{id}`, `payment=true`).
5. Send an image to `/drives/driveOut/`.
6. Verify data via `/drives/getDrivesByPlate/{plate}`.

## Test Notebook

The project includes an API test notebook:

- `app/api/test.ipynb`

You can use it for quick login and `drives` endpoint tests with `httpx`.

## Logging and Security

- Passwords are not stored in plain text; they are hashed with Argon2.
- JWT tokens are validated through the `get_current_user` dependency.
- Protected endpoints require a valid `Authorization` header.

## Roadmap / Possible Improvements

- Enable and enforce RBAC (roles: admin/operator/user).
- Add a Celery task status endpoint by `task_id`.
- Split `access_token` and `refresh_token`.
- Expand automated tests (pytest + integration tests).
- Add Docker Compose for a full local stack (API + Redis + worker + DB).

## License

This project is licensed under MIT. See `LICENSE` for details.
