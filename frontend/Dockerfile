# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Install streamlit
RUN pip install streamlit

# Copy frontend files
COPY . .

# Export port 8501 for Streamlit
EXPOSE 8501

# Run the dashboard
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"]
