import pytest
from fastapi.testclient import TestClient # Используем стандартный клиент FastAPI
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Импорты твоего кода
from src.infrastructure.adapter.in_bound.deck_controller import app, get_db
from src.infrastructure.config.database import Base

@pytest.fixture(scope="session")
def postgres_container():
    """Запускаем контейнер один раз на всю сессию тестов."""
    with PostgresContainer("postgres:14-alpine") as container:
        yield container

@pytest.fixture
def test_db_session(postgres_container):
    """Создаем тестовую БД и сессию для одного теста."""
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)

@pytest.fixture
def client(test_db_session):
    """Создаем тестовый клиент FastAPI, подменяя зависимость БД."""
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    # Подменяем реальную БД на тестовую
    app.dependency_overrides[get_db] = override_get_db
    
    # Используем TestClient вместо httpx напрямую
    with TestClient(app) as c:
        yield c
        
    # Очищаем переопределения после теста
    del app.dependency_overrides[get_db]


def test_full_user_flow(client):
    """Тестируем полный сценарий: создать колоду -> получить её по ID."""
    # 1. Создание колоды (POST)
    response_create = client.post(
        "/decks/",
        json={"title": "E2E Test Deck", "owner_id": "e2e-user"}
    )
    assert response_create.status_code == 201
    deck_data = response_create.json()
    assert deck_data["title"] == "E2E Test Deck"
    deck_id = deck_data["id"]

    # 2. Получение созданной колоды (GET)
    response_get = client.get(f"/decks/{deck_id}")
    assert response_get.status_code == 200
    retrieved_deck = response_get.json()
    assert retrieved_deck["id"] == deck_id
    assert retrieved_deck["title"] == "E2E Test Deck"