from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DomainEvent:
    occurred_at: datetime

@dataclass(frozen=True)
class CardAddedToDeckEvent(DomainEvent):
    deck_id: str
    card_id: str
    term: str

@dataclass(frozen=True)
class CardReviewedEvent(DomainEvent):
    card_id: str
    grade: int
    new_interval: int