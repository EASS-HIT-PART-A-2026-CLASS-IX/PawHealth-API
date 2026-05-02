FROM python:3.12-slim
WORKDIR /app
RUN pip install streamlit httpx
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"]
