import pytest
# Предполагается, что код домена доступен для импорта
from src.domain.models.value_objects import DeckSettings
from src.domain.models.entities import Deck
from src.domain.models.exceptions import DeckArchivedException, InvalidCardContentException
from src.domain.models.events import CardAddedToDeckEvent

@pytest.fixture
def new_deck():
    """Фикстура, которая создает свежий объект колоды для каждого теста."""
    settings = DeckSettings(max_new_cards_per_day=20)
    return Deck(deck_id="d1", title="English B2", settings=settings, owner_id="user1")

def test_add_card_success_generates_event(new_deck):
    # Act
    new_deck.add_card("c1", "Apple", "Яблоко")
    
    # Assert
    assert new_deck.get_cards_count() == 1
    events = new_deck.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], CardAddedToDeckEvent)
    assert events[0].term == "Apple"

def test_cannot_add_duplicate_term(new_deck):
    # Arrange
    new_deck.add_card("c1", "Apple", "Яблоко")
    
    # Act & Assert
    with pytest.raises(InvalidCardContentException, match="уже существует"):
        new_deck.add_card("c2", "Apple", "Другое яблоко")

def test_cannot_add_card_to_archived_deck(new_deck):
    # Arrange
    new_deck.archive_deck()
    
    # Act & Assert
    with pytest.raises(DeckArchivedException):
        new_deck.add_card("c1", "Cat", "Кот")