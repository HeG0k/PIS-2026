from abc import ABC, abstractmethod
from typing import List
# from src.study_service.domain.models.events import DomainEvent

class EventPublisher(ABC):
    @abstractmethod
    def publish_all(self, events: List['DomainEvent']) -> None:
        """Опубликовать доменные события (например, в RabbitMQ)"""
        pass