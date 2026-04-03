from src.application.command.commands import CreateDeckCommand
from src.application.ports.repository import DeckRepository
# Импорты из лабы 3:
# from src.study_service.domain.models.entities import Deck
# from src.study_service.domain.models.value_objects import DeckSettings

class CreateDeckHandler:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, command: CreateDeckCommand) -> str:
        # 1. Создание агрегата
        settings = DeckSettings(max_new_cards_per_day=20) # Дефолтные настройки
        deck = Deck(
            deck_id=command.deck_id, 
            title=command.title, 
            settings=settings, 
            owner_id=command.owner_id
        )
        
        # 2. Сохранение
        self.repository.save(deck)
        
        # Возвращаем только ID (CQRS)
        return deck.id