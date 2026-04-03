import pytest
from src.cqrs.projection.deck_projection import DeckProjectionHandler
from src.cqrs.read_model.deck_view import DeckSummaryView
from src.domain.models.events import CardAddedToDeckEvent
from datetime import datetime

def test_projection_updates_count(db_session):
    # Arrange
    handler = DeckProjectionHandler(db_session)
    deck_id = "deck-1"
    
    # Создаем начальную вьюху
    handler.handle_deck_created(deck_id, "English", "user-1")
    
    # Act: Имитируем событие добавления карточки
    event = CardAddedToDeckEvent(datetime.now(), deck_id, "c1", "Apple")
    handler.handle_card_added(event)
    
    # Assert: Проверяем, что в Read Model счетчик стал 1
    view = db_session.query(DeckSummaryView).filter_by(id=deck_id).first()
    assert view.cards_count == 1