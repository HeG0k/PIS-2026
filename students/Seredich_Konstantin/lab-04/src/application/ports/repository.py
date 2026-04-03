from abc import ABC, abstractmethod
from typing import Optional
# Предполагаем, что Deck импортируется из лабы 3
# from src.study_service.domain.models.entities import Deck

class DeckRepository(ABC):
    @abstractmethod
    def get_by_id(self, deck_id: str) -> Optional['Deck']:
        pass

    @abstractmethod
    def save(self, deck: 'Deck') -> None:
        pass