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
│   ├── main.py          # Intelligence Engine & API Routes
│   ├── models.py        # SQLModel Schemas & Validation Rules
│   ├── database.py      # Persistence Layer (SQLite)
├── tests/
│   ├── conftest.py      # Pytest Fixtures Setup
│   └── test_api.py      # Validation Tests
├── README.md            # Technical Documentation
└── pyproject.toml       # Environment Configuration
\`\`\`

## 🚦 Getting Started

1. **Initialize Environment**:
   \`\`\`bash
   uv sync
   \`\`\`

2. **Launch System**:
   \`\`\`bash
   uv run uvicorn app.main:app --reload
   \`\`\`

3. **Interactive Documentation**:
   Access the full API suite at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🤖 AI Assistance

This project was developed in collaboration with **Gemini (Google)**. AI tools were utilized for:

- Designing the modular project directory structure.
- Implementing SQLModel relationship logic and Field validations.
- Solving StaticPool connection issues in the Pytest suite.
- Generating technical documentation and formatting.

---
**Created by Bar Aizenberg**
