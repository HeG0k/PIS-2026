"""
Notification Service: отправка уведомлений по событиям Event Bus.

События (лаб. №8): GroupAssignedToRequest, RequestActivated → Notification Service
"""
import os

from infrastructure.event_bus.rabbitmq_subscriber import RabbitMQSubscriber


def main():
    subscriber = RabbitMQSubscriber(
        host=os.getenv("RABBITMQ_HOST", "rabbitmq"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        username=os.getenv("RABBITMQ_USER", "admin"),
        password=os.getenv("RABBITMQ_PASS", "password"),
        queue_name="notification_service_queue",
    )

    @subscriber.subscribe("GroupAssignedToRequest")
    def on_group_assigned(payload: dict):
        print(
            "🔔 Уведомление: группа назначена на заявку — "
            f"request_id={payload.get('request_id')}, group_id={payload.get('group_id')}"
        )

    @subscriber.subscribe("RequestActivated")
    def on_request_activated(payload: dict):
        print(
            "🔔 Уведомление: заявка активирована — "
            f"request_id={payload.get('request_id')}, "
            f"group_id={payload.get('group_id')}, zone={payload.get('zone_name')}"
        )

    try:
        subscriber.start_consuming()
    except KeyboardInterrupt:
        subscriber.close()


if __name__ == "__main__":
    main()
