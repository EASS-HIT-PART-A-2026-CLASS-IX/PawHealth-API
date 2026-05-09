# 🐾 PawHealth Pro - Smart Veterinary Management System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org)

**PawHealth Pro** is an enterprise-grade backend solution for comprehensive pet healthcare management. Developed as part of the **EASS-HIT 2026** course, this system provides a robust API for tracking dog profiles, weight metrics, and medical history with strict data validation.

## 🌟 Key Features

- **🐕 Profile Management**: Complete CRUD operations for pet registration and tracking.
- **📊 Smart Health Metrics**: Specialized weight analysis handling cases like Joey (11kg dog, 10kg target) with personalized caloric recommendations.
- **🛡️ Advanced Security**: Full JWT (JSON Web Token) implementation with cryptographic signing and Bearer token validation.
- **🌐 CORS Enabled**: Pre-configured for seamless integration with frontend frameworks.
- **🧪 Automated Testing**: Full suite of 32 tests using pytest with isolated in-memory database execution.

## 🚀 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/dogs` | List all dogs (with pagination) |
| **POST** | `/dogs` | Register a new dog (JWT Protected) |
| **PATCH** | `/dogs/{dog_id}` | Partially update a dog profile |
| **DELETE** | `/dogs/{dog_id}` | Remove a dog profile |
| **POST** | `/health/weight` | Log weight for a specific dog_id |
| **GET** | `/dogs/{dog_id}/weight` | Get weight history & variance analysis |
| **POST** | `/health/feeding` | Log feeding session |
| **GET** | `/healthz` | System and Sidecar health check |

## 🏗 System Architecture

The project follows a clean, modular microservice-ready structure:

~~~text
paw-health-api/
├── app/                 # Backend API (FastAPI + SQLModel)
│   ├── routers/         # Integrated API Routes (Dogs, Health, System)
│   ├── main.py          # Intelligence Engine
│   ├── models.py        # SQLModel Schemas, DTOs & Weight Logic
│   ├── database.py      # Persistence Layer (SQLite & Session Engine)
│   └── security.py      # JWT Signing & Validation
├── frontend/            # Streamlit Interface (EX2 Requirement)
├── sidecar/             # AI Sidecar Microservice (EX3 Requirement)
├── tests/               # 32+ Integration & Unit Tests
├── compose.yaml         # Docker Orchestration (API, UI, Sidecar)
├── pyproject.toml       # Environment & Dependency Configuration
└── README.md            # Technical Documentation
~~~

## 🛠 Tech Stack

- **Framework**: FastAPI (Asynchronous logic)
- **Database**: SQLModel (Modern SQLAlchemy + Pydantic wrapper)
- **Environment Management**: [uv](https://github.com/astral-sh/uv)
- **Security**: PyJWT with HMAC-SHA256
- **Testing**: Pytest with httpx

## 🚦 Getting Started

### Option 1: Docker (Recommended)
Launch the entire ecosystem (API, Sidecar, and UI) with a single command:
~~~bash
docker compose up -d --build
~~~
*   **Management Dashboard:** http://localhost:8501
*   **Interactive API Docs:** http://localhost:8000/docs
*   **System Health Monitor:** http://localhost:8000/healthz

### Option 2: Local Development
~~~bash
uv sync
uv run uvicorn app.main:app --reload
~~~

## 🧪 Running Tests
~~~bash
uv run pytest tests/ -v
~~~

## 🤖 AI Assistance

This project was developed in collaboration with **Gemini (Google)**. AI tools were utilized for designing the modular structure, implementing SQLModel logic, and generating the 32-test suite.

*All AI-generated code was manually reviewed, modified to fit HIT course requirements, and verified through local integration tests.*

---
**Created by Bar Aizenberg** *Passionate about Dog Health & Software Engineering.*
