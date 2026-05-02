# Use python slim image for a smaller footprint
FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Sync dependencies using uv
RUN uv sync --frozen

# Export port 8000 for FastAPI
EXPOSE 8000

# Run the application with uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
