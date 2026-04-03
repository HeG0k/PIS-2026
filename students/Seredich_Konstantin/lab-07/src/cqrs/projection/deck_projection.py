from sqlalchemy.orm import Session
from src.cqrs.read_model.deck_view import DeckSummaryView
from src.domain.models.events import CardAddedToDeckEvent

class DeckProjectionHandler:
    """Синхронизирует Read Model при возникновении событий в Write Model"""
    
    def __init__(self, session: Session):
        self.session = session

    def handle_card_added(self, event: CardAddedToDeckEvent):
        # Когда добавлена карточка, мы просто инкрементируем счетчик в Read Model
        view = self.session.query(DeckSummaryView).filter_by(id=event.deck_id).first()
        if view:
            view.cards_count += 1
            self.session.commit()

    def handle_deck_created(self, deck_id: str, title: str, owner_id: str):
        # Создаем начальную запись в Read Model
        new_view = DeckSummaryView(
            id=deck_id,
            title=title,
            owner_id=owner_id,
            cards_count=0
        )
        self.session.add(new_view)
        self.session.commit()