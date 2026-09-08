# Property & BPO Management System

Operations platform for property preservation and BPO workflows, with property records, vendor work orders, SLA-oriented statuses, and dashboard metrics.

## Features
- Property and client records
- Vendor/work-order workflow
- Priority and status tracking
- Operations dashboard at `/`
- REST API and Swagger at `/docs`
- Health endpoint and automated tests
- Docker-ready deployment

## Stack
Python · FastAPI · Pydantic · PostgreSQL-ready architecture · Docker

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/`.

## Core API
`POST /properties`, `GET /properties`, `POST /work-orders`, `GET /work-orders`, `PATCH /work-orders/{id}`, and `GET /dashboard`.

> Demo workflow application. Add authentication, persistent database storage, audit logging, and organization-specific SLA rules before production use.
