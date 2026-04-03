import unittest
from unittest.mock import Mock, call
from src.application.command.commands import AddCardCommand
from src.application.command.handlers.add_card_handler import AddCardHandler

# Заглушка для агрегата (для теста)
class DummyDeck:
    def __init__(self, id):
        self.id = id
        self.events = ["DummyEvent1"]
    def add_card(self, c_id, term, dfn): pass
    def pull_events(self): return self.events

class TestAddCardHandler(unittest.TestCase):
    def setUp(self):
        # 1. Создаем моки (заглушки) для портов
        self.mock_repo = Mock()
        self.mock_publisher = Mock()
        
        # 2. Инжектим моки в хэндлер
        self.handler = AddCardHandler(self.mock_repo, self.mock_publisher)

    def test_handle_success(self):
        # Arrange (Подготовка)
        command = AddCardCommand("d1", "c1", "Apple", "Яблоко")
        dummy_deck = DummyDeck("d1")
        
        # Настраиваем мок репозитория: при вызове get_by_id вернуть dummy_deck
        self.mock_repo.get_by_id.return_value = dummy_deck

        # Act (Действие)
        self.handler.handle(command)

        # Assert (Проверка)
        # Проверяем, что агрегат был запрошен из БД
        self.mock_repo.get_by_id.assert_called_once_with("d1")
        
        # Проверяем, что агрегат был сохранен
        self.mock_repo.save.assert_called_once_with(dummy_deck)
        
        # Проверяем, что события были отправлены в паблишер
        self.mock_publisher.publish_all.assert_called_once_with(["DummyEvent1"])

if __name__ == '__main__':
    unittest.main()