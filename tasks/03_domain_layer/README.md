# Лабораторная работа №3. Доменный уровень

**Дисциплина:** Проектирование интернет-систем  
**Тема:** Сущности, Value Objects, агрегаты и инварианты

---

> ⚠️ **Важно:** Эта лаба основана на **скелете из Lab #2**. Вы берёте простые модели (Request, Group, Zone) и наполняете их полноценной бизнес-логикой: валидацией, инвариантами, доменными событиями.

---

## Цель работы

Разработать полноценную доменную модель с применением тактических паттернов DDD: сущности, value objects, агрегаты, инварианты и доменные события. Наполнить скелет проекта из Lab #2 реальной бизнес-логикой.

## Результаты обучения

После выполнения работы студент будет:
- Различать Entity и Value Object по критерию идентичности
- Проектировать агрегаты с корректными границами и бизнес-правилами
- Реализовывать бизнес-инварианты через методы агрегата (а не через сеттеры!)
- Создавать доменные события для важных изменений состояния
- Понимать принцип "богатой доменной модели" (rich domain model)

## Связь с предыдущими лабами

- **Lab #1**: Вы моделировали use-cases и sequence diagrams → теперь превращаете их в код
- **Lab #2**: Вы создали скелет проекта с интерфейсами портов → теперь наполняете domain/ полноценными моделями

## Задание

### Часть 1. Определение сущностей (Entities)

Наполните domain/models/ из Lab #2 полноценными сущностями. Добавьте минимум **3 Entity**.

**Примеры для ПСО «Юго-Запад»** (Request Service):
- `Request` (заявка) - REQ-2024-NNNN
- `Group` (группа) - G-01, G-02
- `Volunteer` (участник) - волонтёр в группе
- `Coordinator` (координатор)

**Требования к Entity**:
- ✅ Имеет уникальный идентификатор (ID)
- ✅ Равенство определяется **только** по ID
- ✅ Может изменять состояние (mutable)
- ✅ Бизнес-методы (не просто геттеры/сеттеры!)

**Пример для ПСО: Group (Группа)**

```python
class Group:
    """Entity: Поисковая группа"""
    
    MIN_MEMBERS = 3
    MAX_MEMBERS = 5
    
    def __init__(self, group_id: str, leader_id: str):
        self._id = group_id  # G-01, G-02
        self._leader_id = leader_id
        self._members: List[str] = []  # IDs волонтёров
        self._status = "FORMING"  # FORMING → READY → DEPLOYED
    
    def add_member(self, volunteer_id: str) -> None:
        """Добавить участника в группу"""
        if self._status != "FORMING":
            raise ValueError(f"Нельзя изменить состав группы в статусе {self._status}")
        
        if len(self._members) >= self.MAX_MEMBERS:
            raise ValueError(f"Группа уже содержит максимум участников ({self.MAX_MEMBERS})")
        
        if volunteer_id in self._members:
            raise ValueError(f"Участник {volunteer_id} уже в группе")
        
        self._members.append(volunteer_id)
    
    def mark_ready(self) -> None:
        """Пометить группу как готовую к выходу"""
        if len(self._members) < self.MIN_MEMBERS:
            raise ValueError(f"Группа должна содержать минимум {self.MIN_MEMBERS} участников")
        
        self._status = "READY"
    
    @property
    def member_count(self) -> int:
        return len(self._members)
    
    def __eq__(self, other):
        """Равенство по ID"""
        if not isinstance(other, Group):
            return False
        return self._id == other._id
    
    def __hash__(self):
        return hash(self._id)
```

**Ключевые принципы**:
- ❌ НЕ делайте публичных сеттеров (set_status)
- ✅ Используйте бизнес-методы (mark_ready, add_member)
- ✅ Валидация в методах, а не снаружи
- ✅ Инварианты защищены агрегатом

### Часть 2. Определение Value Objects

Создайте минимум **4 Value Objects**.

**Примеры для ПСО «Юго-Запад»**:
- `Zone` (зона поиска с координатами)
- `RequestStatus` (статус заявки)
- `PhoneNumber` (телефон для SMS)
- `Location` (координаты местоположения)

**Требования к Value Object**:
- ✅ Иммутабельный (immutable) - все поля final/readonly
- ✅ Равенство по значениям **всех** полей
- ✅ Валидация в конструкторе
- ✅ Только геттеры, **НЕТ** сеттеров

**Пример для ПСО: Zone (Зона поиска)**

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)  # frozen=True делает класс immutable
class Zone:
    """Value Object: Зона поиска с координатами"""
    
    name: str  # "North", "South", "East", "West"
    bounds: Tuple[float, float, float, float]  # (lat_min, lat_max, lon_min, lon_max)
    
    def __post_init__(self):
        """Валидация при создании"""
        if not self.name:
            raise ValueError("Zone name cannot be empty")
        
        lat_min, lat_max, lon_min, lon_max = self.bounds
        
        if not (-90 <= lat_min <= 90 and -90 <= lat_max <= 90):
            raise ValueError(f"Latitude must be in range [-90, 90]: {lat_min}, {lat_max}")
        
        if not (-180 <= lon_min <= 180 and -180 <= lon_max <= 180):
            raise ValueError(f"Longitude must be in range [-180, 180]: {lon_min}, {lon_max}")
        
        if lat_min >= lat_max:
            raise ValueError(f"lat_min must be < lat_max: {lat_min} >= {lat_max}")
        
        if lon_min >= lon_max:
            raise ValueError(f"lon_min must be < lon_max: {lon_min} >= {lon_max}")
    
    def contains_point(self, lat: float, lon: float) -> bool:
        """Проверить, находится ли точка в зоне"""
        lat_min, lat_max, lon_min, lon_max = self.bounds
        return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max
    
    # Равенство по всем полям (автоматически в @dataclass)
    # __eq__ и __hash__ генерируются автоматически
```

**Пример: PhoneNumber**

```python
@dataclass(frozen=True)
class PhoneNumber:
    """Value Object: Телефонный номер для SMS"""
    
    number: str  # "+375291234567"
    
    def __post_init__(self):
        if not self.number.startswith("+"):
            raise ValueError("Phone must start with +")
        
        # Убираем + и проверяем что только цифры
        digits = self.number[1:]
        if not digits.isdigit():
            raise ValueError(f"Phone must contain only digits after +: {self.number}")
        
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError(f"Phone length must be 10-15 digits: {len(digits)}")
```

**Ключевые отличия от Entity**:
- Value Object не имеет ID (идентифицируется значениями)
- Два Zone с одинаковыми name и bounds - **одно и то же**
- Два Group с одинаковыми ID но разными members - **одна и та же группа**
```

### Часть 3. Проектирование агрегата

Выберите **корневую сущность** (Aggregate Root) и определите границы агрегата.

**Агрегат = корневая Entity + зависимые Entity/Value Objects**

**Пример для ПСО: Агрегат Request**

```python
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass, field

class Request:
    """Aggregate Root: Заявка на поисково-спасательную операцию"""
    
    def __init__(self, request_id: str, coordinator_id: str, zone: Zone):
        # Корень агрегата
        self._id = request_id  # REQ-2024-0001
        self._coordinator_id = coordinator_id
        self._zone = zone  # Value Object
        
        # Части агрегата (не живут отдельно от Request)
        self._assigned_group: Optional[Group] = None
        self._events: List[DomainEvent] = []  # Доменные события
        
        # Статус и аудит
        self._status = RequestStatus.DRAFT
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    # Инвариант #1: Группа должна быть готова (3-5 участников)
    def assign_group(self, group: Group) -> None:
        """Назначить группу на заявку"""
        if self._status != RequestStatus.DRAFT:
            raise ValueError(
                f"Нельзя назначить группу для заявки в статусе {self._status}"
            )
        
        if group.member_count < 3 or group.member_count > 5:
            raise ValueError(
                f"Группа должна содержать 3-5 участников, текущий размер: {group.member_count}"
            )
        
        self._assigned_group = group
        self._updated_at = datetime.now()
        
        # Доменное событие
        self._events.append(GroupAssignedToRequest(
            request_id=self._id,
            group_id=group.id,
            occurred_at=datetime.now()
        ))
    
    # Инвариант #2: Активировать можно только с назначенной группой
    def activate(self) -> None:
        """Активировать заявку (начать операцию)"""
        if self._assigned_group is None:
            raise ValueError(
                "Нельзя активировать заявку без назначенной группы"
            )
        
        if self._status != RequestStatus.DRAFT:
            raise ValueError(
                f"Заявка уже имеет статус {self._status}"
            )
        
        self._status = RequestStatus.ACTIVE
        self._updated_at = datetime.now()
        
        # Доменное событие
        self._events.append(RequestActivated(
            request_id=self._id,
            group_id=self._assigned_group.id,
            zone_name=self._zone.name,
            occurred_at=datetime.now()
        ))
    
    # Инвариант #3: Нельзя изменить завершённую заявку
    def change_zone(self, new_zone: Zone) -> None:
        """Изменить зону поиска"""
        if self._status == RequestStatus.COMPLETED:
            raise ValueError(
                "Нельзя изменить зону для завершённой заявки"
            )
        
        old_zone_name = self._zone.name
        self._zone = new_zone
        self._updated_at = datetime.now()
        
        self._events.append(RequestZoneChanged(
            request_id=self._id,
            old_zone=old_zone_name,
            new_zone=new_zone.name,
            occurred_at=datetime.now()
        ))
        }
    }

    public void confirm() {
        ensureEditable();
        
        if (lines.isEmpty()) {
            throw new EmptyOrderException(id);
        }
        
        this.status = OrderStatus.CONFIRMED;
        registerEvent(new OrderConfirmedEvent(id, customerId, getTotalAmount()));
    }

    public void cancel(String reason) {
        if (status == OrderStatus.SHIPPED) {
            throw new IllegalStateException("Cannot cancel shipped order");
        }
        
        this.status = OrderStatus.CANCELLED;
        registerEvent(new OrderCancelledEvent(id, reason));
    }

    // Инвариант: сумма заказа = сумме позиций
    public Money getTotalAmount() {
        return lines.stream()
                .map(OrderLine::getSubtotal)
                .reduce(Money.ZERO, Money::add);
    }

    private void ensureEditable() {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Order is not editable");
        }
    }

    // Доменные события
    private final List<DomainEvent> events = new ArrayList<>();

    private void registerEvent(DomainEvent event) {
        events.add(event);
    }

    public List<DomainEvent> getEvents() {
        return Collections.unmodifiableList(events);
    }

    public void clearEvents() {
        events.clear();
    }
}
```

**OrderLine** (часть агрегата, не самостоятельная сущность):

```java
class OrderLine { // Package-private
    private final ProductId productId;
    private int quantity;
    private final Money unitPrice;

    OrderLine(ProductId productId, int quantity, Money unitPrice) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        this.productId = requireNonNull(productId);
        this.quantity = quantity;
        this.unitPrice = requireNonNull(unitPrice);
    }

    void increaseQuantity(int delta) {
        this.quantity += delta;
    }

    Money getSubtotal() {
        return unitPrice.multiply(quantity);
    }

    // Getters
}
```

### Часть 4. Инварианты агрегата

Опишите все бизнес-правила (инварианты) вашего агрегата.

**Примеры инвариантов для Order**:

| Инвариант | Проверка | Исключение |
|-----------|----------|------------|
| Заказ не может быть пустым | `if (lines.isEmpty())` в `confirm()` | `EmptyOrderException` |
| Нельзя изменить подтверждённый заказ | `ensureEditable()` проверяет статус | `IllegalStateException` |
| Максимум 50 позиций в заказе | `if (lines.size() >= MAX_ORDER_LINES)` | `OrderLimitExceededException` |
| Сумма заказа >= 0 | Проверка в `Money.add()` | `IllegalArgumentException` |
| Адрес доставки обязателен | `requireNonNull(address)` в конструкторе | `NullPointerException` |

**Задача**: Составьте таблицу инвариантов для вашего агрегата.

### Часть 5. Доменные события

Определите события, которые происходят при изменении состояния агрегата.

```java
public interface DomainEvent {
    Instant occurredOn();
}

public class OrderConfirmedEvent implements DomainEvent {
    private final OrderId orderId;
    private final CustomerId customerId;
    private final Money totalAmount;
    private final Instant occurredOn;

    public OrderConfirmedEvent(OrderId orderId, CustomerId customerId, Money amount) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.totalAmount = amount;
        this.occurredOn = Instant.now();
    }

    @Override
    public Instant occurredOn() {
        return occurredOn;
    }

    // Getters
}

public class OrderCancelledEvent implements DomainEvent {
    private final OrderId orderId;
    private final String reason;
    private final Instant occurredOn;

    // constructor, getters
}
```

**События для Order**:
- `OrderCreated`
- `OrderLineAdded`
- `OrderConfirmed`
- `OrderCancelled`
- `OrderShipped`

### Часть 6. Юнит-тесты инвариантов

Напишите тесты для проверки бизнес-правил.

```java
class OrderTest {
    
    @Test
    void shouldNotConfirmEmptyOrder() {
        Order order = new Order(customerId, address);
        
        assertThrows(EmptyOrderException.class, () -> order.confirm());
    }

    @Test
    void shouldNotModifyConfirmedOrder() {
        Order order = createOrderWithItems();
        order.confirm();
        
        assertThrows(IllegalStateException.class, () -> 
            order.addLine(productId, 1, price)
        );
    }

    @Test
    void shouldCalculateTotalCorrectly() {
        Order order = new Order(customerId, address);
        order.addLine(product1, 2, new Money(100, "USD"));
        order.addLine(product2, 1, new Money(50, "USD"));
        
        Money total = order.getTotalAmount();
        assertEquals(new Money(250, "USD"), total);
    }

    @Test
    void shouldRegisterEventWhenConfirmed() {
        Order order = createOrderWithItems();
        order.confirm();
        
        List<DomainEvent> events = order.getEvents();
        assertEquals(1, events.size());
        assertTrue(events.get(0) instanceof OrderConfirmedEvent);
    }
}
```

## Критерии оценки

| Критерий | Баллы |
|----------|-------|
| Сущности (Entities) | 15 |
| Value Objects | 15 |
| Агрегат с корректными границами | 25 |
| Инварианты и валидация | 20 |
| Доменные события | 10 |
| Юнит-тесты | 15 |
| **ИТОГО** | **100** |

## Контрольные вопросы

1. В чём разница между Entity и Value Object?
2. Почему OrderLine не является отдельной сущностью?
3. Что произойдёт, если нарушить инвариант агрегата?
4. Зачем регистрировать доменные события?
5. Можно ли изменить Value Object после создания?

## Срок сдачи

**Неделя 6-7 семестра**
