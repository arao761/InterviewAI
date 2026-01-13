# Multi-stage build for InterviewAI Backend
FROM python:3.13-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install ai-engine first (required dependency)
COPY ai-engine/ /app/ai-engine/
WORKDIR /app/ai-engine
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Copy and install backend dependencies
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Runtime stage
FROM python:3.13-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/uploads /app/data /app/logs && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy ai-engine (installed as editable)
COPY --from=builder /app/ai-engine /app/ai-engine

# Copy backend application
COPY backend/ /app/backend/

# Set Python path to include ai-engine
ENV PYTHONPATH=/app/ai-engine/src:/app/backend:$PYTHONPATH

# Create uploads directory
RUN mkdir -p /app/uploads/resumes /app/uploads/audio /app/uploads/exports /app/data/sessions

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Default command (can be overridden in docker-compose)
CMD ["sh", "-c", "cd /app/backend && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
