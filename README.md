# 🐾 PawHealth Pro - Ultimate Veterinary Management (V3.6.1)

**PawHealth Pro** is an enterprise-grade backend solution for comprehensive pet healthcare. Designed for modern veterinary needs, it features a **Smart Intelligence Engine** that actively monitors nutrition, weight trends, and medical schedules to ensure proactive care.

## 🌟 Pro Features

- **🧠 Unified Activity Timeline:** A sophisticated chronological feed that aggregates medical records, feeding logs, and weight entries into a single intelligence stream.
- **📸 Media & Profile Management:** Integrated support for profile picture uploads with secure file validation and static serving.
- **🏥 Clinical Medical Records:** Detailed tracking of vet visits including comprehensive summaries, professional diagnoses, and automated follow-up scheduling.
- **🚨 Emergency SOS Registry:** Instant, high-priority access to pet identification (Chip IDs) and emergency veterinary contact information.
- **🛡️ Data Integrity & Security:** Built with strict SQLModel relational mapping, foreign key enforcement, and Pydantic validation (e.g., Weight > 0).
- **⏱️ Performance Monitoring:** Integrated middleware for real-time request duration logging and system health diagnostics.

## 🏗 System Architecture

The project follows a modular, industry-standard architecture focused on scalability and relational data integrity.

\`\`\`text
paw-health-api/
├── app/
│   ├── main.py          # Intelligence Engine & API Routes
│   ├── models.py        # Relational Schemas & Validation Rules
│   ├── database.py      # Persistence Layer (SQLite)
├── scripts/
│   ├── seed.py          # Automated Data Seeding (Bonus)
├── tests/
│   ├── test_main.py     # Comprehensive Pytest Suite
├── uploads/             # Persistent Image Storage
├── pyproject.toml       # Environment Configuration
└── README.md            # Technical Documentation
\`\`\`

## 🛠 Tech Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI (Asynchronous logic)
- **Database:** SQLModel (Modern SQLAlchemy + Pydantic wrapper)
- **Environment:** uv (Fast Python package manager)
- **Dependency:** python-multipart (For secure file handling)

## 🚦 Getting Started

1. **Initialize Environment:**
   \`\`\`bash
   uv sync
   \`\`\`

2. **Populate Demo Data (Bonus):**
   \`\`\`bash
   PYTHONPATH=. uv run python scripts/seed.py
   \`\`\`

3. **Launch System:**
   \`\`\`bash
   uv run uvicorn app.main:app --reload
   \`\`\`

4. **Run Automated Tests:**
   \`\`\`bash
   uv run pytest
   \`\`\`

> **Interactive Documentation:** Access the full API suite and SOS registry at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📝 Design Philosophy

Developed for the **EASS-HIT** course, this project demonstrates advanced concepts in RESTful API design, database normalization, and business logic automation. 

Created by **Bar Aizenberg** - Passionate about Dog Health & Software Engineering.

## 🤖 AI Assistance

This project was developed in collaboration with Gemini (Google). AI assisted in:
- Designing the relational database architecture and SQLModel relationship logic.
- Implementing the Unified Timeline aggregation and sorting algorithms.
- Configuring the Pytest suite for robust validation and error-code verification.
*All AI-generated components were manually reviewed, refactored, and verified through automated tests.*
