# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Install minimal requirements
RUN pip install fastapi uvicorn

# Copy sidecar logic
COPY main.py .

# Export port 8001 for the sidecar
EXPOSE 8001

# Start the mock AI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
