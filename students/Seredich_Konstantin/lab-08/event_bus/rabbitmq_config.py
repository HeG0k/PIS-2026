"""
Параметры Event Bus (RabbitMQ) для микросервисов ПСО «Юго-Запад».
"""
EXCHANGE_NAME = "pso_events"
EXCHANGE_TYPE = "topic"

DEFAULT_HOST = "rabbitmq"
DEFAULT_PORT = 5672
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "password"
