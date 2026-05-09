FROM python:3.12-slim
WORKDIR /app
RUN pip install streamlit httpx pandas
COPY . .
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
