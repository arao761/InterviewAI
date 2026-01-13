# Docker Setup Guide for InterviewAI

This guide explains how to use Docker to run InterviewAI locally and in production.

## Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Create Environment File

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key-here
# Add other required environment variables
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 4. Stop Services

```bash
docker-compose down
```

To also remove volumes (database data):
```bash
docker-compose down -v
```

## Development Mode

For development with hot reload:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This mounts your code as volumes, enabling:
- Backend auto-reload on code changes
- Frontend hot reload (if configured)

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend sh

# Run database migrations manually
docker-compose exec backend alembic upgrade head

# Frontend shell
docker-compose exec frontend sh
```

### Rebuild After Changes

```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

## Database Management

### Access PostgreSQL

```bash
docker-compose exec postgres psql -U postgres -d prepwise_db
```

### Run Migrations

Migrations run automatically on backend startup. To run manually:

```bash
docker-compose exec backend alembic upgrade head
```

### Create New Migration

```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

### Backup Database

```bash
docker-compose exec postgres pg_dump -U postgres prepwise_db > backup.sql
```

### Restore Database

```bash
docker-compose exec -T postgres psql -U postgres prepwise_db < backup.sql
```

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, 5432, or 6379 are already in use:

1. Stop the conflicting service
2. Or change ports in `docker-compose.yml`:
   ```yaml
   ports:
     - "8001:8000"  # Use 8001 instead of 8000
   ```

### Backend Won't Start

1. Check logs: `docker-compose logs backend`
2. Verify database is healthy: `docker-compose ps`
3. Check environment variables in `.env`
4. Ensure `ai-engine` is properly installed

### Frontend Build Fails

1. Check Node.js version (should be 22)
2. Clear build cache: `docker-compose build --no-cache frontend`
3. Check `next.config.mjs` for configuration issues

### Database Connection Issues

1. Verify PostgreSQL is running: `docker-compose ps postgres`
2. Check connection string in `DATABASE_URL`
3. Ensure migrations have run: `docker-compose logs backend | grep alembic`

## Production Deployment

### Build for Production

```bash
docker-compose -f docker-compose.yml build
```

### Environment Variables

Create `.env.production` with production values:
- `ENVIRONMENT=production`
- `DEBUG=false`
- Strong `SECRET_KEY`
- Production database URL
- Production API keys

### Run Production

```bash
docker-compose --env-file .env.production up -d
```

## Architecture

```
┌─────────────┐
│  Frontend   │ (Next.js on port 3000)
│  (port 3000)│
└──────┬───────┘
       │
       │ HTTP requests
       │
┌──────▼───────┐
│   Backend    │ (FastAPI on port 8000)
│  (port 8000) │
└──┬────────┬──┘
   │        │
   │        │
┌──▼──┐  ┌─▼───┐
│Postgres│ │Redis│
│ :5432 │ │:6379│
└──────┘ └─────┘
```

## Volumes

Data is persisted in Docker volumes:
- `postgres_data`: Database files
- `redis_data`: Redis cache
- `./backend/uploads`: Uploaded files (mounted from host)

## Network

All services are on the `interviewai-network` bridge network and can communicate using service names:
- Backend → PostgreSQL: `postgres:5432`
- Backend → Redis: `redis:6379`
- Frontend → Backend: `backend:8000`

## Security Notes

1. **Never commit `.env` files** - they contain secrets
2. **Use strong SECRET_KEY** in production
3. **Limit CORS_ORIGINS** to your domain
4. **Use production database** with SSL
5. **Enable HTTPS** in production

## Next Steps

- Set up CI/CD with Docker images
- Deploy to cloud platforms (AWS ECS, Google Cloud Run, etc.)
- Add monitoring and logging
- Set up automated backups
