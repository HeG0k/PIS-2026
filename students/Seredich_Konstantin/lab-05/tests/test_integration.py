import unittest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.adapter.out_bound.deck_repository import DeckRepositoryImpl, DeckOrmModel, metadata

class TestDeckRepositoryIntegration(unittest.TestCase):

    def setUp(self):
        # Запускаем временный Docker контейнер с PostgreSQL
        self.postgres_container = PostgresContainer("postgres:14-alpine").start()
        db_url = self.postgres_container.get_connection_url()
        
        # Подключаемся к тестовой БД
        self.engine = create_engine(db_url)
        metadata.create_all(self.engine) # Создаем таблицы
        
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        # Останавливаем контейнер после теста
        self.postgres_container.stop()

    def test_save_and_get_deck(self):
        # Arrange
        session = self.Session()
        repo = DeckRepositoryImpl(session)
        
        # Имитация доменного объекта
        deck_to_save = type('Deck', (object,), {
            'id': 'test-deck-1', 
            '_title': 'My Test Deck', 
            '_owner_id': 'user-1'
        })()
        
        # Act
        repo.save(deck_to_save)
        retrieved_deck = repo.get_by_id('test-deck-1')
        
        # Assert
        self.assertIsNotNone(retrieved_deck)
        self.assertEqual(retrieved_deck.title, 'My Test Deck')
        
        session.close()

if __name__ == '__main__':
    unittest.main()