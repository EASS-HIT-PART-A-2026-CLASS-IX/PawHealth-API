# 🐾 PawHealth Pro - Smart Veterinary Management System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org)

**PawHealth Pro** is an enterprise-grade backend solution for comprehensive pet healthcare. Developed as part of the **EASS-HIT 2026** course, this system provides a robust API for tracking dog profiles, weight metrics, and medical history.

## 🌟 Key Features
- **🐕 Profile Management**: Complete CRUD operations for pet registration and tracking.
- **📊 Health Metrics**: Specialized logging for weight with automated Pydantic validation.
- **🛡️ Data Integrity**: Powered by **SQLModel**, ensuring type safety between the API and the database.
- **🌐 CORS Enabled**: Pre-configured for seamless integration with frontend frameworks.
- **🧪 Automated Testing**: Full test suite using `pytest` with isolated in-memory database execution.

## 🏗 System Architecture
\`\`\`text
paw-health-api/
├── app/
│   ├── main.py          # API Routes
│   ├── models.py        # SQLModel Schemas
│   ├── database.py      # Persistence Layer
├── tests/
│   ├── conftest.py      # Pytest Fixtures
│   └── test_api.py      # Integration Tests
└── README.md            # Technical Documentation
\`\`\`

## 🛠 Tech Stack
- **Framework**: FastAPI
- **Database**: SQLModel (SQLite)
- **Environment**: [uv](https://github.com/astral-sh/uv)
- **Testing**: Pytest

## 🚦 Getting Started
1. **Initialize**: \`uv sync\`
2. **Seed Data**: \`uv run python seed.py\`
3. **Run Server**: \`uv run uvicorn app.main:app --reload\`

## 🤖 AI Assistance
This project was developed in collaboration with **Gemini (Google)**. AI assisted in modular architecture design, SQLModel validation rules, and Pytest configuration. All code was manually verified and tested locally.

---
**Created by Bar Aizenberg**
