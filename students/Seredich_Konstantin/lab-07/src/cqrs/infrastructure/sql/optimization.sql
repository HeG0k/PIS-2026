-- 1. Индекс для быстрого получения колод конкретного пользователя
CREATE INDEX idx_deck_summaries_owner ON deck_summaries (owner_id);

-- 2. Пример запроса, который теперь работает мгновенно (O(1) вместо O(N))
-- Мы не используем COUNT(*) и JOIN, а берем готовое число
SELECT title, cards_count 
FROM deck_summaries 
WHERE owner_id = 'user-123' AND is_archived = FALSE;

-- 3. Как проверить эффективность (команда для отчета)
EXPLAIN ANALYZE SELECT * FROM deck_summaries WHERE owner_id = 'user-123';