FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app.py, core/, utils/, api/, config/
COPY . .

# the compose file chooses the process:
#   python app.py                                   (monitoring loop)
#   uvicorn api.status_api:app --host 0.0.0.0 --port 8000   (status API)
CMD ["python", "app.py"]
