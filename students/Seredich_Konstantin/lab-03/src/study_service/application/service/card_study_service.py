from study_service.application.port.in_bound.review_card_use_case import ReviewCardUseCase, ReviewCardCommand
from study_service.application.port.out_bound.card_repository import CardRepository

class CardStudyService(ReviewCardUseCase):
    """Сервис приложения: оркестрирует выполнение use-case"""
    
    def __init__(self, card_repository: CardRepository):
        # Инъекция зависимости (DIP): сервис зависит от абстракции, а не от конкретной БД
        self.card_repository = card_repository

    def review_card(self, command: ReviewCardCommand) -> bool:
        # 1. Достаем сущность (Domain) из БД через порт (Infrastructure)
        card = self.card_repository.get_by_id(command.card_id)
        if not card:
            return False
            
        # 2. Вызываем чистую бизнес-логику (Domain)
        card.record_review(command.is_correct)
        
        # 3. Сохраняем изменения через порт
        self.card_repository.save(card)
        return True