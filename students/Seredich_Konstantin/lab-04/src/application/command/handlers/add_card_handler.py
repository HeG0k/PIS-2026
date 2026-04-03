from src.application.command.commands import AddCardCommand
from src.application.ports.repository import DeckRepository
from src.application.ports.event_publisher import EventPublisher

class AddCardHandler:
    def __init__(self, repository: DeckRepository, event_publisher: EventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def handle(self, command: AddCardCommand) -> None:
        # 1. Загрузка агрегата
        deck = self.repository.get_by_id(command.deck_id)
        if not deck:
            raise ValueError(f"Колода с ID {command.deck_id} не найдена")

        # 2. Вызов бизнес-логики агрегата
        deck.add_card(command.card_id, command.term, command.definition)

        # 3. Сохранение (Транзакция)
        self.repository.save(deck)

        # 4. Публикация доменных событий (Side-effects)
        events = deck.pull_events()
        self.event_publisher.publish_all(events)
        
        # Ничего не возвращаем (CQRS)