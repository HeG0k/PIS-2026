# Лабораторная работа №7. CQRS и Read Models (Разделение чтения/записи)

**Дисциплина:** Проектирование интернет-систем  
**Тема:** CQRS, Event Sourcing, Materialized Views

---

## Цель работы

Реализовать **CQRS** с разделением моделей:
- **Write Model** - агрегаты (Request)
- **Read Model** - денормализованные проекции для запросов

---

## Результаты обучения

- **Применять** CQRS паттерн
- **Создавать** Read Models (проекции)
- **Синхронизировать** модели через доменные события
- **Оптимизировать** запросы

---

## Задание

### Часть 1. Разделение моделей

**Write Model** (сохраняет Request):
- Нормализованная структура
- Инварианты, события

**Read Model** (RequestView):
- Денормализованная структура
- Оптимизация для чтения

📖 **Пример:** [examples/cqrs/read_model/request_view.py](examples/cqrs/read_model/request_view.py)

---

### Часть 2. Event-Driven Synchronization

При сохранении Request → публикация `RequestCreated` → обновление `RequestView`.

📖 **Пример:** [examples/cqrs/projection/request_projection.py](examples/cqrs/projection/request_projection.py)

---

### Часть 3. Оптимизация запросов

**Индексы, материализованные представления.**

📖 **Пример:** [examples/sql/materialized_view.sql](examples/sql/materialized_view.sql)

---

<!-- START:artifacts -->
## Структура отчёта

📄 **[Макет отчёта →](Макет_отчета.md)**

```
lab-07/
├── Отчет.md
├── cqrs/
│   ├── write_model/       # Request (aggregate)
│   ├── read_model/        # RequestView (projection)
│   └── projection/        # Event handlers
└── tests/
    └── test_projection.py
```
<!-- END:artifacts -->

<!-- START:criteria -->
## Критерии оценки

| Критерий | Баллы | Требования |
|----------|-------|------------|
| Write Model: агрегат с инвариантами | 20 | Request из Lab #3 |
| Read Model: денормализация | 25 | RequestView с joins |
| Event-Driven Sync: проекции | 25 | Обработка событий |
| Оптимизация запросов | 15 | Индексы, EXPLAIN |
| Тесты проекций | 10 | Проверка синхронизации |
| Качество документации | 5 | Диаграммы, README |
| **ИТОГО** | **100** | |
<!-- END:criteria -->

<!-- START:bonuses -->
## Бонусы (+ до 15)

* **Event Sourcing** (+6) - хранение событий вместо состояния
* **Materialized Views (PostgreSQL)** (+5) - автообновление
* **Redis для Read Model** (+4) - кэш для запросов
<!-- END:bonuses -->

## Контрольные вопросы

1. **В чём разница между CQRS и CQS?**
2. **Почему Read Model денормализованная?**
3. **Как синхронизировать модели при сбое?**
4. **Что такое Eventual Consistency?**

---

## Срок сдачи

**Неделя 14-15 семестра**
