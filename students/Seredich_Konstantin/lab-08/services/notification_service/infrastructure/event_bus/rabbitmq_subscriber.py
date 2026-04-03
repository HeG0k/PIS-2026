"""
RabbitMQ Subscriber: Notification Service

Предметная область: ПСО «Юго-Запад»
"""
import json
from typing import Callable, Dict

import pika

from event_bus.rabbitmq_config import (
    DEFAULT_HOST,
    DEFAULT_PASSWORD,
    DEFAULT_PORT,
    DEFAULT_USER,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
)


class RabbitMQSubscriber:
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        username: str = DEFAULT_USER,
        password: str = DEFAULT_PASSWORD,
        queue_name: str = "notification_service_queue",
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

        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)

        print(f"✅ Notification Service connected to RabbitMQ at {host}:{port}")

        self.handlers: Dict[str, Callable] = {}

    def subscribe(self, event_type: str, routing_key: str | None = None):
        if routing_key is None:
            routing_key = event_type

        self.channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=self.queue_name,
            routing_key=routing_key,
        )

        print(f"🔗 Notification subscribed to: {routing_key}")

        def decorator(handler: Callable):
            self.handlers[event_type] = handler
            return handler

        return decorator

    def start_consuming(self):
        def callback(ch, method, properties, body):
            try:
                event_data = json.loads(body)
                event_type = event_data.get("event_type")

                handler = self.handlers.get(event_type)
                if handler:
                    handler(event_data["payload"])
                else:
                    print(f"⚠️ No handler for event: {event_type}")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                print(f"❌ Error processing event: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
        )

        print("📥 Notification Service listening...")
        self.channel.start_consuming()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("🔌 RabbitMQ connection closed")
