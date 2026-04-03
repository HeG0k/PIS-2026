import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Импорты из Лабы 5
from src.infrastructure.adapter.out_bound.deck_repository import DeckRepositoryImpl
from src.infrastructure.config.database import Base # Берем Base отсюда

@pytest.fixture(scope="module")
def postgres_container():
    """Фикстура, которая запускает Docker контейнер для всех тестов в модуле."""
    with PostgresContainer("postgres:14-alpine") as container:
        yield container

@pytest.fixture
def db_session(postgres_container):
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    
    # Используем Base.metadata вместо старого импорта
    Base.metadata.create_all(engine) 
    
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    
    Base.metadata.drop_all(engine)

def test_save_and_get_deck(db_session):
    # Arrange
    repo = DeckRepositoryImpl(db_session)
    deck_to_save = type('Deck', (object,), {
        'id': 'test-deck-1', '_title': 'My Test Deck', '_owner_id': 'user-1'
    })()
    
    # Act
    repo.save(deck_to_save)
    retrieved_deck = repo.get_by_id('test-deck-1')
    
    # Assert
    assert retrieved_deck is not None
    assert retrieved_deck.title == 'My Test Deck'