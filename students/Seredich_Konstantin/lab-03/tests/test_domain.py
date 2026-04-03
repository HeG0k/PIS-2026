import unittest
from src.study_service.domain.models.value_objects import DeckSettings, CardContent, ReviewGrade
from src.study_service.domain.models.entities import Deck
from src.study_service.domain.models.exceptions import DeckArchivedException, InvalidCardContentException
from src.study_service.domain.models.events import CardAddedToDeckEvent

class TestDeckAggregate(unittest.TestCase):

    def setUp(self):
        settings = DeckSettings(max_new_cards_per_day=20)
        self.deck = Deck(deck_id="d1", title="English B2", settings=settings, owner_id="user1")

    def test_add_card_success_generates_event(self):
        self.deck.add_card("c1", "Apple", "Яблоко")
        
        self.assertEqual(self.deck.get_cards_count(), 1)
        events = self.deck.pull_events()
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], CardAddedToDeckEvent)
        self.assertEqual(events[0].term, "Apple")

    def test_cannot_add_duplicate_term(self):
        self.deck.add_card("c1", "Apple", "Яблоко")
        with self.assertRaises(InvalidCardContentException):
            # Пытаемся добавить карточку с таким же термином
            self.deck.add_card("c2", "Apple", "Другое яблоко")

    def test_cannot_add_card_to_archived_deck(self):
        self.deck.archive_deck()
        with self.assertRaises(DeckArchivedException):
            self.deck.add_card("c1", "Cat", "Кот")

    def test_value_object_validation(self):
        # Невалидный контент
        with self.assertRaises(ValueError):
            CardContent(term="", definition="test")
            
        # Невалидная оценка (больше 4)
        with self.assertRaises(ValueError):
            ReviewGrade(5)

if __name__ == '__main__':
    unittest.main()