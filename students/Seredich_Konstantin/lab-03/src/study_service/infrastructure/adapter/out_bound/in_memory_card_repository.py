from study_service.application.port.out_bound.card_repository import CardRepository
from study_service.domain.models.card import Card

class InMemoryCardRepository(CardRepository):
    """Адаптер БД: Простая in-memory реализация для демонстрации"""
    
    def __init__(self):
        self._db = {}  # Имитация таблицы БД
        # Добавим тестовую карточку
        test_card = Card(card_id="card-123", term="Apple", definition="Яблоко")
        self._db["card-123"] = test_card

    def get_by_id(self, card_id: str) -> Card:
        return self._db.get(card_id)

    def save(self, card: Card) -> None:
        self._db[card.card_id] = card
        print(f"[DB LOG] Карточка {card.card_id} сохранена. Следующее повторение: {card.next_review}")