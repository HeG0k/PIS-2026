from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, String, Integer, MetaData
from sqlalchemy.orm import registry
# Для простоты, здесь же определим ORM модель и интерфейс
# В реальном проекте они были бы в разных файлах

# === ORM Модель (Как данные хранятся в таблице) ===
metadata = MetaData()
mapper_registry = registry()

deck_table = Table(
    'decks', metadata,
    Column('id', String(50), primary_key=True),
    Column('title', String(100), nullable=False),
    Column('owner_id', String(50), nullable=False)
)

# Модель, которую мы будем использовать в репозитории
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