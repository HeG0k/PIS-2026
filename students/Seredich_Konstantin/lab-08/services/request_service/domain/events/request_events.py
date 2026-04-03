"""События заявки для Request Service. ПСО «Юго-Запад»."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Tuple

from domain.events.domain_event import DomainEvent


@dataclass
class RequestCreated(DomainEvent):
    request_id: str
    coordinator_id: str
    zone_name: str
    zone_bounds: Tuple[float, float, float, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "coordinator_id": self.coordinator_id,
            "zone_name": self.zone_name,
            "zone_bounds": list(self.zone_bounds),
        }


@dataclass
class GroupAssignedToRequest(DomainEvent):
    request_id: str
    group_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "group_id": self.group_id,
        }


@dataclass
class RequestActivated(DomainEvent):
    request_id: str
    group_id: str
    zone_name: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "group_id": self.group_id,
            "zone_name": self.zone_name,
        }
