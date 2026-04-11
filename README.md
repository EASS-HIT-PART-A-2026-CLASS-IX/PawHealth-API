# 🐾 PawHealth Pro - Smart Veterinary Management System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org)

**PawHealth Pro** is an enterprise-grade backend solution for comprehensive pet healthcare management. Developed as part of the **EASS-HIT 2026** course, this system provides a robust API for tracking dog profiles, weight metrics, and medical history with strict data validation.

## 🌟 Key Features

- **🐕 Profile Management**: Complete CRUD operations for pet registration and tracking.

- **📊 Health Metrics**: Specialized logging for weight with automated Pydantic validation.

- **🛡️ Data Integrity**: Powered by **SQLModel**, ensuring type safety between the API and the database.

- **🌐 CORS Enabled**: Pre-configured for seamless integration with frontend frameworks.

- **🧪 Automated Testing**: Full test suite using `pytest` with isolated in-memory database execution.

## 🏗 System Architecture

The project follows a clean, modular microservice-ready structure:

```text
paw-health-api/
├── app/
│   ├── main.py          # Intelligence Engine & API Routes
│   ├── models.py        # SQLModel Schemas & Validation Rules
│   ├── database.py      # Persistence Layer (SQLite & Session Engine)
├── tests/
│   ├── conftest.py      # Pytest Fixtures & StaticPool Setup
│   └── test_api.py      # Integration and Validation Tests
├── pawhealth.db         # Local SQLite Database (Auto-generated)
├── pyproject.toml       # Environment & Dependency Configuration
└── README.md            # Technical Documentation
```

## 🛠 Tech Stack

- **Framework**: FastAPI (Asynchronous logic)
- **Database**: SQLModel (Modern SQLAlchemy + Pydantic wrapper)
- **Environment Management**: [uv](https://github.com/astral-sh/uv)
- **Testing**: Pytest with `httpx`

## 🚦 Getting Started

### 1. Initialize Environment
Ensure you have `uv` installed, then run:

```bash
uv sync
```

### 2. Launch the Server

```bash
uv run uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 3. Interactive Documentation
Access the auto-generated Swagger UI to test the endpoints:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Running Tests

```bash
uv run pytest
```

## 🤖 AI Assistance

This project was developed in collaboration with **Gemini (Google)**. AI tools were utilized for:

- Designing the modular project directory structure.
- Implementing complex SQLModel relationship logic and `Field` validations.
- Solving `StaticPool` connection issues in the Pytest suite.
- Generating technical documentation and formatting.

*All AI-generated code was manually reviewed, modified to fit HIT course requirements, and verified through local integration tests.*

---
**Created by Bar Aizenberg** *Passionate about Dog Health & Software Engineering.*
