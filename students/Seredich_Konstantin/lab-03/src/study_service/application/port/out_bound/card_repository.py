from abc import ABC, abstractmethod
from study_service.domain.models.card import Card

class CardRepository(ABC):
    """Исходящий порт: интерфейс для работы с хранилищем (БД)"""
    
    @abstractmethod
    def get_by_id(self, card_id: str) -> Card:
        """Получить карточку по ID"""
        pass

    @abstractmethod
    def save(self, card: Card) -> None:
        """Сохранить изменения карточки"""
        pass