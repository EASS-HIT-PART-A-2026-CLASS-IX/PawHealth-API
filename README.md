# 🐾 PawHealth Pro - Smart Veterinary Management System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org)

**PawHealth Pro** is an enterprise-grade backend solution for comprehensive pet healthcare management. Developed as part of the **EASS-HIT 2026** course, this system provides a robust API for tracking dog profiles, weight metrics, and medical history with strict data validation and clinical-grade health analysis.

## 🌟 Key Features

- **🐕 Profile Management**: Complete CRUD operations for pet registration and lifecycle tracking.
- **📊 Clinical Health Metrics**: Advanced variance analysis comparing current weight against ideal targets to generate automated caloric and exercise recommendations.
- **🛡️ Advanced Security**: Professional JWT (JSON Web Token) implementation featuring cryptographic signing, automated expiration, and Bearer token validation.
- **🌐 Frontend Integration**: Pre-configured CORS support and RESTful endpoints for seamless interface connectivity.
- **🧪 High-Coverage Testing**: Full suite of 32 automated integration tests ensuring 100% functionality across security, persistence, and business logic.

## 🚀 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/dogs` | List all dog profiles (with pagination) |
| **POST** | `/dogs` | Register a new profile (JWT Protected) |
| **PATCH** | `/dogs/{id}` | Partially update profile metrics |
| **DELETE** | `/dogs/{id}` | Securely remove a profile |
| **POST** | `/health/weight` | Log weight metrics for telemetry |
| **GET** | `/dogs/{id}/weight` | Retrieve weight history and variance analysis |
| **POST** | `/health/feeding` | Log nutritional intake sessions |
| **GET** | `/healthz` | Multi-service stack health monitoring |

## 🏗 System Architecture

The project follows a clean, modular microservice-ready structure:

~~~text
paw-health-api/
├── app/                 # Backend API (FastAPI + SQLModel)
│   ├── routers/         # Integrated API Routes (Dogs, Health, System)
│   ├── main.py          # Intelligence Engine & Core Logic
│   ├── models.py        # SQLModel Schemas, DTOs & Domain Logic
│   ├── database.py      # Persistence Layer (SQLite & Session Engine)
│   └── security.py      # JWT Signing & Auth Middleware
├── frontend/            # Streamlit Interface (UI Tier)
├── sidecar/             # AI Intelligence Service (Sidecar Tier)
├── tests/               # 32+ Integration and Validation Tests
├── compose.yaml         # Docker Orchestration for all services
└── pyproject.toml       # Environment & Dependency Configuration
~~~

## 🛠 Tech Stack

- **Framework**: FastAPI (Asynchronous logic)
- **Database**: SQLModel (Modern SQLAlchemy + Pydantic wrapper)
- **Environment Management**: [uv](https://github.com/astral-sh/uv)
- **Security**: PyJWT with HMAC-SHA256 signing
- **Testing**: Pytest with asynchronous HTTPX support

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
Run each service in a separate terminal:

**Terminal 1 — Backend API:**
~~~bash
uv sync
uv run uvicorn app.main:app --reload
~~~

**Terminal 2 — Sidecar:**
~~~bash
pip install fastapi uvicorn
cd sidecar && uvicorn main:app --port 8001 --reload
~~~

**Terminal 3 — Frontend:**
~~~bash
pip install streamlit httpx pandas
streamlit run frontend/app.py
~~~

*   **Management Dashboard:** http://localhost:8501
*   **Interactive API Docs:** http://localhost:8000/docs
*   **System Health Monitor:** http://localhost:8000/healthz

## 🧪 Running Tests
~~~bash
uv run pytest tests/ -v
~~~

## 🤖 AI Assistance

This project was developed in collaboration with **Gemini (Google)**. AI tools were utilized for architectural design, SQLModel logic optimization, and generating the comprehensive 32-test suite.

*All AI-generated code was manually reviewed, modified to fit HIT course requirements, and verified through local integration tests.*

---
**Created by Bar Aizenberg** *Passionate about Dog Health & Software Engineering.*
