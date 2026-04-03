from src.application.query.queries import GetDeckByIdQuery, DeckReadDto
from src.application.ports.repository import DeckRepository

class GetDeckByIdHandler:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, query: GetDeckByIdQuery) -> DeckReadDto:
        deck = self.repository.get_by_id(query.deck_id)
        if not deck:
            raise ValueError(f"Колода с ID {query.deck_id} не найдена")
            
        # Преобразуем Domain Entity в Read DTO (без изменения состояния)
        return DeckReadDto(
            id=deck.id,
            title=deck._title,
            cards_count=deck.get_cards_count(),
            is_archived=deck._is_archived
        )