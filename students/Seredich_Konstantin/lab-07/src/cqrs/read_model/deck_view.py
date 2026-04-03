from sqlalchemy import Column, String, Integer, Boolean
from src.infrastructure.config.database import Base

class DeckSummaryView(Base):
    """Денормализованная модель для быстрого чтения списка колод"""
    __tablename__ = "deck_summaries"
    extend_existing = True

    id = Column(String(50), primary_key=True)
    title = Column(String(100))
    owner_id = Column(String(50), index=True) # Индекс для быстрого поиска по юзеру
    cards_count = Column(Integer, default=0)  # Денормализованное поле (уже посчитано)
    is_archived = Column(Boolean, default=False)