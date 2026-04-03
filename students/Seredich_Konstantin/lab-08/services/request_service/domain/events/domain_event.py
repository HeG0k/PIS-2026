"""Базовый класс доменного события для публикации в Event Bus."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class DomainEvent:
    """Доменное событие с идентификатором и меткой времени."""

    event_id: str
    occurred_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError
