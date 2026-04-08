# 🐾 PawHealth API - Professional Dog Health Registry

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org)

**PawHealth API** is a high-performance, agent-ready backend system designed for tracking and monitoring canine health, nutrition, and medical history. Built with a focus on data integrity and real-time insights.

## 🚀 Key Features
- **Dog Profile Management**: Digital identity including breed and chip identification.
- **Nutrition Tracking**: Logging daily food intake with data validation.
- **Weight SOC (Security Operations Center)**: Continuous monitoring of weight changes.
- **Medical Registry**: Tracking vaccinations and identifying overdue treatments.
- **Alert & Analytics Engine**: Automated insights into pet health trends.
- **Request Middleware**: Professional logging for performance monitoring (execution time in ms).

## 🛠 Tech Stack
- **Framework**: FastAPI (Python 3.12+)
- **Database/ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Persistence**: SQLite (Local file-based storage)
- **Tooling**: `uv` for lightning-fast package management

## 📂 Project Structure
```text
paw-health-api/
├── app/
│   ├── main.py          # Server entry point & Middleware
│   ├── models.py        # Database schemas & Validation
│   ├── database.py      # Connection & Session management
├── paw_health.db        # Persistent SQLite database
├── pyproject.toml       # Dependencies
└── README.md            # Documentation
```

## 🚦 Quick Start
1. **Install dependencies**:
   ```bash
   uv sync
   ```
2. **Start the API server**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```
3. **Explore interactive docs**:
   Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📊 Monitoring & Performance
The system includes a custom Middleware that logs every incoming request with detailed timing, similar to enterprise-grade security monitoring systems (HomeSOC inspiration).

---
*Developed as part of the EASS-HIT course.*
