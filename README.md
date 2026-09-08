# Property & BPO Management System

Professional workflow platform for property preservation and BPO operations.

## Core modules
- Properties and owners
- Vendors and assignments
- Work orders and SLA tracking
- Status workflow and priorities
- Dashboard-ready REST API
- PostgreSQL-ready data layer design

## Stack
Python · FastAPI · SQLAlchemy · PostgreSQL · Docker

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/docs`.
