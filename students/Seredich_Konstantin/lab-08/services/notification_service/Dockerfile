FROM python:3.11-slim

WORKDIR /app

COPY services/notification_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY event_bus /app/event_bus
COPY services/notification_service /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
