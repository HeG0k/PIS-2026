FROM python:3.11-slim

WORKDIR /app

COPY services/group_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY event_bus /app/event_bus
COPY services/group_service /app

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
