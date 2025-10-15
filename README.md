# Local Airtable-Like Platform

This repository contains a full-stack starter for building a local, Airtable-inspired workspace. The backend is powered by Django REST Framework with JWT authentication, dynamic base schemas, and analytics endpoints. A React frontend (to be added) can consume the documented API to deliver spreadsheet-like experiences, role-aware dashboards, and collaborative record management.

## Features

- **Authentication & Roles** – Custom user model with Master, Admin, and Viewer hierarchies plus JWT auth endpoints.
- **Dynamic Base Builder** – Create bases with configurable fields, membership assignments, and per-base permissions.
- **Record Management** – JSON-backed records with validation enforced from field definitions.
- **Analytics** – Per-base and global insights with caching hooks for fast dashboards.
- **API Documentation** – Automatic OpenAPI schema and Swagger UI via drf-spectacular.

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Optional: Node.js 18+ (for the upcoming React frontend)

### Backend Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp backend/.env.example backend/.env
```

Update `backend/.env` with your database credentials and desired secrets.

Run database migrations and create a superuser:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

### API Endpoints

- `POST /api/auth/register/` – User registration
- `POST /api/auth/token/` – Obtain JWT access/refresh tokens
- `GET /api/users/` – Master-only user management
- `GET /api/bases/` – List accessible bases
- `GET /api/bases/<id>/records/` – CRUD records for a base
- `GET /api/bases/<id>/analytics/` – Base-level aggregations
- `GET /api/analytics/global/` – Global dashboard metrics
- `GET /api/docs/` – Interactive Swagger UI

### Frontend (Coming Soon)

The React client will live under `frontend/` and integrate with the endpoints above using TanStack Table, Plotly, and TailwindCSS. Contributions are welcome!

## Testing

Run the Django test suite:

```bash
cd backend
python manage.py test
```

## License

This project is released under the MIT License. See `LICENSE` for details.
