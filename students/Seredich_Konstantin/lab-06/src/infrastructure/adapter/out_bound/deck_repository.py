from sqlalchemy import Table, Column, String, Integer
from sqlalchemy.orm import registry, Session
from src.infrastructure.config.database import Base # Импортируем общую базу

# 1. Вместо создания новых метаданных, привязываем реестр к метаданным Base
mapper_registry = registry(metadata=Base.metadata)

# 2. В определении таблицы заменяем локальный metadata на Base.metadata
deck_table = Table(
    'decks', 
    Base.metadata,  # <--- КРИТИЧЕСКИ ВАЖНО: используем общую метадату
    Column('id', String(50), primary_key=True),
    Column('title', String(100), nullable=False),
    Column('owner_id', String(50), nullable=False),
    extend_existing=True
)

# Дальше код остается без изменений
class DeckOrmModel:
    pass

mapper_registry.map_imperatively(DeckOrmModel, deck_table)

# === Реализация Репозитория ===
# Предполагаем, что интерфейс и доменные сущности доступны.
# Для простоты можно скопировать их определения из прошлых лаб.

class DeckRepositoryImpl: # implements DeckRepository
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, deck_id: str): # -> Optional[Deck]
        # Загрузка из БД
        orm_deck = self.session.query(DeckOrmModel).filter_by(id=deck_id).first()
        if not orm_deck:
            return None
        # Маппинг ORM -> Domain
        # return Deck(id=orm_deck.id, title=orm_deck.title, owner_id=orm_deck.owner_id)
        return orm_deck # Для простоты вернем ORM

    def save(self, deck) -> None: # deck: Deck
        # Маппинг Domain -> ORM
        orm_deck = DeckOrmModel()
        orm_deck.id = deck.id
        orm_deck.title = deck._title # Допустим, title приватный
        orm_deck.owner_id = deck._owner_id
        
        # Сохранение в БД
        self.session.add(orm_deck)
        self.session.commit()