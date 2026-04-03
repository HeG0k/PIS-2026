"""
RabbitMQ Publisher: Публикация событий из Request Service

Предметная область: ПСО «Юго-Запад»
"""
import json
from typing import Any, Dict

import pika

from domain.events.domain_event import DomainEvent
from event_bus.rabbitmq_config import (
    DEFAULT_HOST,
    DEFAULT_PASSWORD,
    DEFAULT_PORT,
    DEFAULT_USER,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
)


class RabbitMQPublisher:
    """
    Publisher для RabbitMQ

    Паттерн: Event Bus
    Ответственность: Публикация доменных событий в RabbitMQ
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        username: str = DEFAULT_USER,
        password: str = DEFAULT_PASSWORD,
    ):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type=EXCHANGE_TYPE,
            durable=True,
        )

        print(f"✅ Connected to RabbitMQ at {host}:{port}")

    def publish(self, event: DomainEvent):
        event_type = event.__class__.__name__
        routing_key = event_type

        payload = self._serialize_event(event)

        self.channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json",
            ),
        )

        print(f"📤 Event published: {event_type} → {routing_key}")

    def publish_dict(self, event_type: str, payload: Dict[str, Any]):
        self.channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=event_type,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json",
            ),
        )

        print(f"📤 Event published: {event_type}")

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("🔌 RabbitMQ connection closed")

    def _serialize_event(self, event: DomainEvent) -> Dict[str, Any]:
        return {
            "event_id": event.event_id,
            "event_type": event.__class__.__name__,
            "occurred_at": event.occurred_at.isoformat(),
            "payload": event.to_dict(),
        }
