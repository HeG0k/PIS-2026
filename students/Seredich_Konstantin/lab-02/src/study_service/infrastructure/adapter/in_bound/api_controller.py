from study_service.application.port.in_bound.review_card_use_case import ReviewCardUseCase, ReviewCardCommand

class CardController:
    """Адаптер API: Имитирует REST контроллер (принимает HTTP запросы)"""
    
    def __init__(self, use_case: ReviewCardUseCase):
        self.use_case = use_case

    def handle_review_request(self, card_id: str, is_correct: bool):
        # Превращаем данные из "интернета" во внутреннюю команду DTO
        command = ReviewCardCommand(card_id=card_id, is_correct=is_correct)
        
        # Передаем управление в Application слой
        success = self.use_case.review_card(command)
        
        if success:
            print(f"[API RESPONSE] 200 OK: Ответ на карточку {card_id} записан.")
        else:
            print(f"[API RESPONSE] 404 Not Found: Карточка не найдена.")