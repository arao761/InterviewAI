# 🐳 Quick Start with Docker

Get InterviewAI running in 3 steps!

## Step 1: Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Make sure Docker is running

## Step 2: Setup

```bash
# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd InterviewAI

# Create .env file
cp .env.example .env

# Edit .env and add your OPENAI_API_KEY
# You can use any text editor:
nano .env
# or
code .env
```

Required in `.env`:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Start

```bash
# Option A: Use the startup script
./docker-start.sh

# Option B: Manual start
docker-compose up -d
```

That's it! 🎉

## Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build
```

## Troubleshooting

**Port already in use?**
- Stop other services using ports 3000, 8000, 5432, or 6379
- Or change ports in `docker-compose.yml`

**Backend won't start?**
```bash
docker-compose logs backend
```

**Database connection issues?**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres
```

## Next Steps

- Read [DOCKER.md](DOCKER.md) for detailed documentation
- Set up development mode with hot reload
- Configure production deployment
