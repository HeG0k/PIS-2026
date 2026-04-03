import pytest
from unittest.mock import Mock
# Импорты из прошлых лаб
from src.application.command.commands import AddCardCommand
from src.application.command.handlers.add_card_handler import AddCardHandler

# Заглушка для доменного объекта, чтобы тест не зависел от него
class DummyDeck:
    def __init__(self, id):
        self.id = id
        self.events = ["DummyEvent1"]
    def add_card(self, c_id, term, dfn): pass
    def pull_events(self): return self.events

def test_add_card_handler_success():
    # Arrange
    mock_repo = Mock()
    mock_publisher = Mock()
    handler = AddCardHandler(mock_repo, mock_publisher)
    
    command = AddCardCommand("d1", "c1", "Apple", "Яблоко")
    dummy_deck = DummyDeck("d1")
    mock_repo.get_by_id.return_value = dummy_deck

    # Act
    handler.handle(command)

    # Assert
    mock_repo.get_by_id.assert_called_once_with("d1")
    mock_repo.save.assert_called_once_with(dummy_deck)
    mock_publisher.publish_all.assert_called_once_with(["DummyEvent1"])