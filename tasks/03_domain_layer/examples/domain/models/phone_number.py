"""
Domain Layer: PhoneNumber (Телефонный номер)

Value Object: Телефонный номер для SMS-уведомлений
Предметная область: ПСО «Юго-Запад»
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class PhoneNumber:
    """
    Value Object: Телефонный номер
    
    Формат: +375XXXXXXXXX (международный формат)
    
    Invariants:
        - Начинается с '+'
        - Содержит только цифры после '+'
        - Длина 10-15 цифр
    """
    
    number: str
    
    def __post_init__(self):
        """Валидация при создании"""
        if not self.number.startswith("+"):
            raise ValueError(
                f"Phone number must start with '+': {self.number}"
            )
        
        # Убираем + и проверяем что только цифры
        digits = self.number[1:]
        if not digits.isdigit():
            raise ValueError(
                f"Phone number must contain only digits after '+': {self.number}"
            )
        
        # Проверка длины
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError(
                f"Phone number must be 10-15 digits, got {len(digits)}: {self.number}"
            )
    
    @property
    def country_code(self) -> str:
        """
        Получить код страны (первые 1-3 цифры)
        
        Например: +375 → "375" (Беларусь)
        """
        digits = self.number[1:]
        
        # Попытка определить длину кода страны
        if digits.startswith("375"):  # Беларусь
            return "375"
        elif digits.startswith("7"):  # Россия
            return "7"
        elif digits.startswith("380"):  # Украина
            return "380"
        else:
            # По умолчанию берём первые 3 цифры
            return digits[:3]
    
    @property
    def national_number(self) -> str:
        """
        Получить номер без кода страны
        
        Например: +375291234567 → "291234567"
        """
        country_code = self.country_code
        return self.number[1 + len(country_code):]
    
    def format_for_display(self) -> str:
        """
        Форматированный вывод для отображения
        
        Например: +375291234567 → "+375 (29) 123-45-67"
        """
        if self.country_code == "375":  # Беларусь
            national = self.national_number
            if len(national) == 9:
                # +375 29 123-45-67
                return f"+375 ({national[:2]}) {national[2:5]}-{national[5:7]}-{national[7:]}"
        
        # По умолчанию просто добавляем пробелы
        return f"+{self.country_code} {self.national_number}"
    
    # Равенство и хэш генерируются автоматически в @dataclass
    # Два PhoneNumber с одинаковым number - ОДНО И ТО ЖЕ
