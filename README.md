# Novexium Website

Production-ready Python web application built with FastAPI, PostgreSQL, Redis, and Docker.

## Architecture

- **FastAPI** - Modern web framework
- **Jinja2** - Template engine
- **Tailwind CSS** - Styling
- **PostgreSQL** - Database
- **Redis** - Cache & session management
- **Celery** - Background jobs
- **Docker** - Containerization
- **Kubernetes** - Orchestration

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload


### Create `docker-compose.yml`:
```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: docker/app/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/novexium
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=novexium
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
