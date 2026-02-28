# Лабораторная работа №6. Testing Strategy (Стратегия тестирования)

**Дисциплина:** Проектирование интернет-систем  
**Тема:** Юнит-тесты, интеграционные тесты, E2E-тесты

---

## Цель работы

Создать комплексную **стратегию тестирования** для Request Service:
- **Юнит-тесты** - домен, handlers
- **Интеграционные тесты** - БД, API
- **E2E-тесты** - полный сценарий

---

## Результаты обучения

- **Применять** Test Pyramid
- **Писать** юнит-тесты с мокерами (pytest, unittest.mock)
- **Настраивать** интеграционные тесты (testcontainers)
- **Автоматизировать** E2E-тесты (Playwright/Selenium)

---

## Задание

### Часть 1. Юнит-тесты Domain Layer

📖 **Пример:** [examples/tests/unit/domain/test_request_aggregate.py](examples/tests/unit/domain/test_request_aggregate.py)

### Часть 2. Юнит-тесты Application Layer

📖 **Пример:** [examples/tests/unit/application/test_create_request_handler.py](examples/tests/unit/application/test_create_request_handler.py)

### Часть 3. Интеграционные тесты

📖 **Пример:** [examples/tests/integration/test_request_repository.py](examples/tests/integration/test_request_repository.py)

### Часть 4. E2E-тесты

📖 **Пример:** [examples/tests/e2e/test_request_flow.py](examples/tests/e2e/test_request_flow.py)

---

<!-- START:artifacts -->
## Структура отчёта

📄 **[Макет отчёта →](Макет_отчета.md)**

```
lab-06/
├── Отчет.md
└── tests/
    ├── unit/
    │   ├── test_domain.py
    │   └── test_handlers.py
    ├── integration/
    │   └── test_repository.py
    └── e2e/
        └── test_request_flow.py
```
<!-- END:artifacts -->

<!-- START:criteria -->
## Критерии оценки

| Критерий | Баллы | Требования |
|----------|-------|------------|
| Юнит-тесты Domain: инварианты, события | 25 | pytest, 100% покрытие |
| Юнит-тесты Application: handlers, mocker | 20 | Mock repository |
| Интеграционные тесты БД: testcontainers | 25 | Реальная PostgreSQL |
| E2E-тесты: полный сценарий | 20 | Create → Assign → Activate |
| CI/CD: автоматический запуск | 5 | GitHub Actions |
| Качество документации | 5 | README по запуску |
| **ИТОГО** | **100** | |
<!-- END:criteria -->

<!-- START:bonuses -->
## Бонусы (+ до 15)

* **Coverage > 90%** (+5) - pytest-cov
* **Mutation Testing** (+5) - mutmut
* **Performance Tests** (+3) - Locust
* **Contract Testing** (+2) - Pact
<!-- END:bonuses -->

## Контрольные вопросы

1. **В чём разница между юнит-тестом и интеграционным?**
2. **Почему юнит-тестов должно быть больше, чем E2E?**
3. **Зачем использовать testcontainers вместо in-memory БД?**
4. **Что тестирует Mutation Testing?**

---

## Срок сдачи

**Неделя 12-13 семестра**
