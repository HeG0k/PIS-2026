from abc import ABC, abstractmethod

class ReviewCardCommand:
    """DTO для передачи данных снаружи внутрь"""
    def __init__(self, card_id: str, is_correct: bool):
        self.card_id = card_id
        self.is_correct = is_correct

class ReviewCardUseCase(ABC):
    """Входящий порт: интерфейс для взаимодействия системы с внешним миром"""
    
    @abstractmethod
    def review_card(self, command: ReviewCardCommand) -> bool:
        """Обработать ответ пользователя на карточку"""
        pass