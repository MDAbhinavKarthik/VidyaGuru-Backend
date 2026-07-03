# VidyaGuru Backend — Docker Development Guide

This guide explains how to develop and run the `vidyaguru-backend` service locally using Docker Compose.

## Prerequisites
- Docker & Docker Desktop installed
- Git

## Getting Started

1. **Start the Dev Environment**:
   ```bash
   docker-compose up --build -d
   ```
   This launches PostgreSQL, Redis, and the FastAPI application with live-reload enabled.

2. **Check Logs**:
   ```bash
   docker-compose logs -f backend
   ```

3. **Run Database Migrations inside container**:
   ```bash
   docker-compose exec backend alembic -c scripts/alembic/alembic.ini upgrade head
   ```

4. **Run Automated Tests**:
   ```bash
   docker-compose exec backend pytest
   ```

5. **Stop Containers**:
   ```bash
   docker-compose down
   ```
