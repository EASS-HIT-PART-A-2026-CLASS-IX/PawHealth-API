# 🐾 PawHealth Pro - Ultimate Veterinary Management System

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-latest-red.svg)
![uv](https://img.shields.io/badge/managed%20by-uv-purple.svg)

**PawHealth Pro** is an enterprise-grade backend microservice designed for comprehensive pet healthcare management. It features a **Smart Intelligence Engine** that aggregates clinical data, nutrition, and weight trends into a unified proactive care system.

---

## 🌟 Key Features

* **🧠 Unified Activity Timeline:** A sophisticated chronological engine that merges medical, feeding, and weight data into a single intelligence feed.
* **📸 Profile Media Management:** Secure image upload and static serving for pet profile pictures with file-type validation.
* **🏥 Clinical Medical Records:** Detailed tracking of veterinary visits including summaries, professional diagnoses, and follow-up schedules.
* **🚨 Emergency SOS Registry:** Instant, high-priority access to chip identification and emergency veterinary contacts.
* **🛡️ Data Integrity:** Strict relational mapping using SQLModel with foreign key enforcement and Pydantic validation (e.g., Weight > 0).
* **⏱️ Performance Diagnostics:** Integrated middleware logging request duration for high-traffic environment monitoring.

---

## 🏗 System Architecture

The project follows a modular architecture inspired by scalable microservices, focusing on separation of concerns and data persistence.

```text
paw-health-api/
├── app/
│   ├── main.py          # API Engine, Routes & Intelligence Logic
│   ├── models.py        # Relational SQLModel Schemas
│   ├── database.py      # Persistence Layer & SQLite Connection
│   └── __init__.py
├── scripts/
│   └── seed.py          # Automated Database Seeding (Bonus)
├── tests/
│   ├── test_main.py     # Comprehensive Pytest Suite
│   └── __init__.py
├── uploads/             # Persistent Profile Image Storage
├── pyproject.toml       # Dependency & Environment Configuration
└── README.md            # Technical Documentation
cat << 'EOF' > README.md
# 🐾 PawHealth Pro - Ultimate Veterinary Management System

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-latest-red.svg)
![uv](https://img.shields.io/badge/managed%20by-uv-purple.svg)

**PawHealth Pro** is an enterprise-grade backend microservice designed for comprehensive pet healthcare management. It features a **Smart Intelligence Engine** that aggregates clinical data, nutrition, and weight trends into a unified proactive care system.

---

## 🌟 Key Features

* **🧠 Unified Activity Timeline:** A sophisticated chronological engine that merges medical, feeding, and weight data into a single intelligence feed.
* **📸 Profile Media Management:** Secure image upload and static serving for pet profile pictures with file-type validation.
* **🏥 Clinical Medical Records:** Detailed tracking of veterinary visits including summaries, professional diagnoses, and follow-up schedules.
* **🚨 Emergency SOS Registry:** Instant, high-priority access to chip identification and emergency veterinary contacts.
* **🛡️ Data Integrity:** Strict relational mapping using SQLModel with foreign key enforcement and Pydantic validation (e.g., Weight > 0).
* **⏱️ Performance Diagnostics:** Integrated middleware logging request duration for high-traffic environment monitoring.

---

## 🏗 System Architecture

The project follows a modular architecture inspired by scalable microservices, focusing on separation of concerns and data persistence.

```text
paw-health-api/
├── app/
│   ├── main.py          # API Engine, Routes & Intelligence Logic
│   ├── models.py        # Relational SQLModel Schemas
│   ├── database.py      # Persistence Layer & SQLite Connection
│   └── __init__.py
├── scripts/
│   └── seed.py          # Automated Database Seeding (Bonus)
├── tests/
│   ├── test_main.py     # Comprehensive Pytest Suite
│   └── __init__.py
├── uploads/             # Persistent Profile Image Storage
├── pyproject.toml       # Dependency & Environment Configuration
└── README.md            # Technical Documentation

🛠 Tech Stack
Language: Python 3.12+ (Typed)

Web Framework: FastAPI (Asynchronous logic)

ORM: SQLModel (Modern SQLAlchemy + Pydantic wrapper)

Package Manager: uv (High-performance dependency resolution)

Testing: Pytest with FastAPI TestClient

🚦 Getting Started
1. Initialize Environment
Bash
uv sync
2. Populate Demo Data (Bonus)
Bash
PYTHONPATH=. uv run python scripts/seed.py
3. Launch the API
Bash
uv run uvicorn app.main:app --reload
4. Execute Test Suite
Bash
uv run pytest
Interactive Documentation: Once the server is running, access the full Swagger UI at: http://127.0.0.1:8000/docs

📝 Design Philosophy
Developed as part of the EASS-HIT course, this project demonstrates advanced concepts in RESTful API design, database normalization, and automated business logic.

Created by Bar Aizenberg - Passionate about Dog Health & Software Engineering.

🤖 AI Assistance
This project was developed in collaboration with Gemini (Google). AI assisted in:

Designing the relational database architecture and SQLModel relationship logic.

Implementing the Unified Timeline aggregation and sorting algorithms.

Configuring the Pytest suite for robust validation and error-code verification.

All AI-generated components were manually reviewed, refactored, and verified through automated tests.
