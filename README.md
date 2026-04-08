# 🐾 PawHealth Pro - Smart Veterinary Management System (V3.0.0)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/ORM-SQLModel-blue?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org)

**PawHealth Pro** is an enterprise-grade backend solution for comprehensive pet healthcare. Unlike standard registries, it features a **Smart Task Engine** that actively monitors nutrition and medical schedules to ensure proactive care.

## 🌟 Pro Features
- **🧠 Smart Task Engine**: Automatically generates a daily checklist (e.g., "Joey needs 50g more food today", "Rabies vaccine due this week").
- **🏥 Clinical Medical Records**: Detailed tracking of vet visits including summaries, diagnoses, and follow-up schedules.
- **🚨 Emergency SOS Registry**: Instant access to emergency veterinary contacts and chip identification.
- **📊 Real-time Health Analytics**: Aggregated insights into average feeding habits and weight trends.
- **🛡️ Data Integrity**: Strict Pydantic validation for all health metrics (Weight > 0, non-empty records).
- **⏱️ Performance Monitoring**: Integrated middleware logging request duration in milliseconds for high-frequency environments.

## 🏗 System Architecture
The project follows a modular architecture inspired by **Security Operations Centers (SOC)**, focusing on event logging and proactive alerting.

```text
paw-health-api/
├── app/
│   ├── main.py          # Intelligence Engine & API Routes
│   ├── models.py        # Relational Schemas & Validation Rules
│   ├── database.py      # Persistence Layer (SQLite)
├── paw_health.db        # Production Database
├── pyproject.toml       # Environment Configuration
└── README.md            # Technical Documentation
```

## 🛠 Tech Stack
- **Language**: Python 3.12+
- **Framework**: FastAPI (Asynchronous logic)
- **Database**: SQLModel (Modern SQLAlchemy + Pydantic wrapper)
- **Log Management**: Python Logging with Custom Middleware

## 🚦 Getting Started
1. **Initialize Environment**:
   ```bash
   uv sync
   ```
2. **Launch System**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```
3. **Interactive Documentation**:
   Access the full API suite at `http://127.0.0.1:8000/docs`

## 📝 Design Philosophy
Developed for the **EASS-HIT** course, this project demonstrates advanced concepts in **RESTful API design**, **Database Normalization**, and **Business Logic Automation**.

---
*Created by Bar Aizenberg - Passionate about Dog Health & Software Engineering.*

## 🤖 AI Assistance
This project was developed in collaboration with Gemini (Google). AI assisted in:
- Designing the modular project architecture.
- Implementing SQLModel schemas and relationship logic.
- Configuring the Pytest suite with `StaticPool` for isolated DB testing.
All outputs were manually reviewed, integrated, and verified through automated tests.
